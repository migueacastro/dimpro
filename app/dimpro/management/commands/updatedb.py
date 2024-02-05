import os
from alegra.client import Client

from django.db.utils import IntegrityError
from django.core.management.base import BaseCommand, CommandError, CommandParser
from dimpro.models import ItemQuantity, Product, AlegraUser
import time 
import schedule

class Command(BaseCommand):
    help = 'Populates and updates database from Alegra List'

    def handle(self, *args, **options):
        def update():
            def add_data(it, det, ref, avq):
                d, created = Product.objects.get_or_create(item=it, details=det, reference=ref, available_quantity=avq)
                return d

            alegra_user = AlegraUser.objects.get(id=1)
            client = Client(alegra_user.email, alegra_user.token)

            itemquantity = ItemQuantity.objects.get(id=1)
            n = (int(itemquantity.quantity) // 30) 
            items = []

            
            

            for i in range(n):

                dictu = client.list_items(start=(n * 10 * i), order="ASC")
                items = items + dictu
            
            for row in items:
                item = row['name']
                details = row['description']
                reference = row['reference']
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
                    

                    selecteditem.save()
                    self.stdout.write(self.style.SUCCESS('Sucessfully updated item "%s"' % reference))
                except Product.DoesNotExist:
                    try:
                        add_data(item, details, reference, available_quantity)
                        self.stdout.write(self.style.SUCCESS('Succesfully added item "%s"' % reference))
                        
                    except IntegrityError as e:
                        self.stdout.write(self.style.ERROR('Error: Product "%s" already exists: "%s"' % (reference, e)))
                        continue
        schedule.every(30).minutes.do(update)
        while True:
            schedule.run_pending()
            time.sleep(1)
            
            