from django.contrib import admin
from .models import User, Image, Product, AlegraUser, Order, Order_Product, Contact
# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'last_name', 'email')
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'reference', 'item')
class AlegraUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email')
class OrderAdmmin(admin.ModelAdmin):
    list_display = ('id', 'client_id', 'user_email', 'date')
class Order_ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'order_id', 'product_id', 'quantity')
class ContactAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


admin.site.register(Contact, ContactAdmin)
admin.site.register(Order, OrderAdmmin)
admin.site.register(Order_Product, Order_ProductAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Image)
admin.site.register(AlegraUser, AlegraUserAdmin)