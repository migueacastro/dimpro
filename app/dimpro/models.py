from typing import Any
from django.contrib.auth.models import UserManager, AbstractBaseUser, PermissionsMixin, timezone
from django.db import models
from django.db.models import Count
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
import datetime
# Create your models here.
class CustomUserManager(UserManager):
    def _create_user(self, email, password, phonenumber, **extra_fields):
        if not email:
            raise ValueError("No has ingresado una direccion e-mail valida.")
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.phonenumber = phonenumber
        user.save(using=self._db)

        return user
    
    def create_user(self, email=None, password=None, phonenumber=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_operator', False)
        return self._create_user(email, password, phonenumber, **extra_fields)
    
    def create_superuser(self, email=None, password=None, phonenumber=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_operator', True)
        return self._create_user(email, password, phonenumber,**extra_fields)
    
    def create_staff(self, email=None, password=None, phonenumber=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_operator', False)
        return self._create_user(email, password, phonenumber,**extra_fields)
    
class User(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(blank=True, default='', unique=True)
    name = models.CharField(max_length=255, blank=True, default='')
    last_name = models.CharField(max_length=255, blank=True, default='')
    phoneregex = RegexValidator(regex=r"^\+?58?\d{11,15}$")
    phonenumber = models.CharField(
        validators=[phoneregex], max_length=17, blank=True, null=False
    )
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_operator = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(blank=True, null=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
    
    def get_full_name(self):
        return self.name
    
    def get_short_name(self):
        return self.name or self.email.split('@')[0]
    
    def user_orders(self):
        return Order.objects.filter(user_email=self.id).count()
    
class Product(models.Model):
    item = models.CharField(max_length=64, unique=False)
    id = models.AutoField(primary_key=True)
    details = models.CharField(max_length=128, null = True)
    reference = models.CharField(max_length=64, unique=True, null = True)
    available_quantity = models.IntegerField(validators = [
        MinValueValidator(1)
    ])
    def __str__(self):
        return str(self.id)

class Image(models.Model):
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    url = models.CharField(max_length=256)

class AlegraUser(models.Model):
    email = models.CharField(max_length=128)
    token = models.CharField(max_length=256)

    
class Contact(models.Model):
    name = models.CharField(max_length=128)
    date_joined = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return str(self.id)
    
class Order(models.Model):
    user_email = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    status = models.CharField(max_length=16,choices= [
        ('preparado', 'Preparado'),
        ('pendiente', 'Pendiente')
    ])
    client_id = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name='orders')
    date = models.DateTimeField(auto_now_add=True)
    def product_categories(self):
        return Order_Product.objects.filter(order_id=self.id).count()
    
    def __str__(self):
        return str(self.id)



class Order_Product(models.Model):
    id = models.AutoField(primary_key=True)
    order_id =  models.ForeignKey(Order, on_delete=models.CASCADE, related_name='orders')
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='orders')
    quantity = models.IntegerField(validators = [
        MinValueValidator(1)
    ])
    def __str__(self):
        return str(self.id)
