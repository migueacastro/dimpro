import os
from alegra.client import Client as c

from django.db.utils import IntegrityError
from django.core.management.base import BaseCommand, CommandError, CommandParser
from dimpro.models import Product, AlegraUser, Contact
from django.core.exceptions import ObjectDoesNotExist
import time 
import schedule

class Command(BaseCommand):
    help = 'Populates and updates database from Alegra List'

    def handle(self, *args, **options):
        def update():
            def add_data(it, det, ref, avq):
                d, created = Product.objects.get_or_create(item=it, details=det, reference=ref, available_quantity=avq)
                return d

            def add_contact(nam):
                d, reated = Contact.objects.get_or_create(name=nam)
                return d
            
            alegra_user = AlegraUser.objects.get(id=1)
            client = c(alegra_user.email, alegra_user.token)

            items = []
         
            i = 0
            while (True):
                
                dictu = client.list_items(start=(30 * i + 1), order="ASC")
                if not dictu:
                    break;
                items = items + dictu
                i += 1
            
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
                except ObjectDoesNotExist:
                    try:
                        add_data(item, details, reference, available_quantity)
                        self.stdout.write(self.style.SUCCESS('Succesfully added item "%s"' % reference))
                        
                    except IntegrityError as e:
                        self.stdout.write(self.style.ERROR('Error: Product "%s" already exists: "%s"' % (reference, e)))
                        continue

            contacts = []
         
            i = 0
            while (True):
                
                dictu = client.list_contacts(start=(30 * i + 1), order="ASC")
                if not dictu:
                    break;
                contacts = contacts + dictu
                i += 1
            
            for row in contacts:
                name = row['name']
                
                
                try:
                    selectedcontact = Contact.objects.get(name=name)
                except ObjectDoesNotExist:
                    try:
                        add_contact(name)
                        self.stdout.write(self.style.SUCCESS('Succesfully added contact "%s"' % name))
                        
                    except Exception as e:
                        self.stdout.write(self.style.ERROR('Error with contact "%s": "%s"' % (name, e)))
                        continue

        schedule.every(30).minutes.do(update)
        while True:
            schedule.run_pending()
            time.sleep(1)
            
def update():
            
            def add_contact(nam):
                d, reated = Contact.objects.get_or_create(name=nam)
                return d
             
            def add_data(it, det, ref, avq):
                d, created = Product.objects.get_or_create(item=it, details=det, reference=ref, available_quantity=avq)
                return d

            alegra_user = AlegraUser.objects.get(id=1)
            client = c(alegra_user.email, alegra_user.token)

            items = []
    
            i = 0
            while (True):
                
                dictu = client.list_items(start=(30 * i + 1), order="ASC")
                if not dictu:
                    break;
                items = items + dictu
                i += 1
            
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
                except ObjectDoesNotExist:
                    try:
                        add_data(item, details, reference, available_quantity)
                        
                    except IntegrityError as e:
                        continue

            contacts = []
         
            i = 0
            while (True):
                
                dictu = client.list_contacts(start=(30 * i + 1), order="ASC")
                if not dictu:
                    break;
                contacts = contacts + dictu
                i += 1
            
            for row in contacts:
                name = row['name']
                try:
                    selectedcontact = Contact.objects.get(name=name)
                except ObjectDoesNotExist:
                    try:
                        add_contact(name) 
                    except Exception as e:
                        continue