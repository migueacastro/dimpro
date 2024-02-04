from django.contrib import admin
from .models import User, Image, Product, ItemQuantity
# Register your models here.

admin.site.register(User)
admin.site.register(Image)
admin.site.register(Product)
admin.site.register(ItemQuantity)