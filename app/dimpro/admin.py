from django.contrib import admin
from .models import User, Image, Product, ItemQuantity, AlegraUser, Order
# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email')
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'reference', 'item')
class ItemQuantityAdmin (admin.ModelAdmin):
    list_display = ('quantity','id')
class AlegraUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email')
class OrderAdmmin(admin.ModelAdmin):
    list_display = ('id', 'product_id', 'user_email', 'date')

admin.site.register(Order, OrderAdmmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Image)
admin.site.register(ItemQuantity, ItemQuantityAdmin)
admin.site.register(AlegraUser, AlegraUserAdmin)