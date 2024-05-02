from alegra.client import Client as c
from django.db.utils import IntegrityError
from dimpro.models import Product, AlegraUser, Contact, PriceType
from django.core.exceptions import ObjectDoesNotExist
            
def update():
            
            def add_contact(nam):
                d, reated = Contact.objects.get_or_create(name=nam, active=True)
                return d
             
            def add_data(it, det, ref, avq, pr):
                d, created = Product.objects.get_or_create(item=it, details=det, reference=ref, available_quantity=avq, price=pr)
                return d

            alegra_user = AlegraUser.objects.get(id=1)
            client = c(alegra_user.email, alegra_user.token)

            items = []
    
            i = 0
            while (True):
                
                dictu = client.list_items(start=(30 * i), order="ASC")
                if not dictu:
                    break;
                items = items + dictu
                i += 1
            
            for row in items:
                item = row['name']
                details = row['description']
                reference = row['reference']
                price = row['price'][0]['price']

                # Check if item exists to avoid duplicates
                try:
                    check = Product.objects.get(reference=reference)
                    continue
                except Product.DoesNotExist:
                    check = None
                

                # Calculate prices in percentages
                
                
                # Add the current prices of Alegra
                if row['name'] == 'BOMBILLO LED 12W' or row['name'] == 'CINTA LED 110V 5.5MM':
                    # Delete all prices
                    PriceType.objects.all().delete()
                    for i in range(len(row["price"])):
                        # Check if the price is from EPA
                        if row['price'][i]['name'] == 'EPA':
                            continue

                        name = row['price'][i]['name']
                        percentage = (row['price'][0]['price'] - row['price'][i]['price']) * 100 / row['price'][0]['price']
                        
                        if percentage == 0:
                            default = True
                        else:
                            default = False
                            
                        PriceType.objects.create(id=i, name=name, percentage=percentage, default =default)


                try:
                    available_quantity = row['inventory']['availableQuantity']
                except KeyError as e:
                    available_quantity = 0
                
                try:
                    selecteditem = Product.objects.get(reference=reference)
                    selecteditem.item = item
                    
                    try:
                        selecteditem.details = details
                    except Product.IntegrityError as e:
                        continue
                
                    selecteditem.reference = reference
                    selecteditem.available_quantity = available_quantity
                    selecteditem.price = price

                    selecteditem.save()
                except ObjectDoesNotExist:
                    try:
                        add_data(item, details, reference, available_quantity, price)
                        
                    except IntegrityError as e:
                        continue

            contacts = []
         
            i = 0
            while (True):
                
                dictu = client.list_contacts(start=(30 * i), order="ASC")
                if not dictu:
                    break
                contacts = contacts + dictu
                i += 1
            
            for row in contacts:
                name = row['name']

                # Check if contact is in alegra db
                list_contacts = Contact.objects.all()
                for contact in list_contacts:
                    if not contact in row:
                        row['active'] = False
                    row['active'] = False

                try:
                    selectedcontact = Contact.objects.get(name=name)
                except ObjectDoesNotExist:
                    try:
                        add_contact(name) 
                    except Exception as e:
                        continue