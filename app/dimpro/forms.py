from django import forms
from phonenumber_field.formfields import PhoneNumberField
from django.core.validators import RegexValidator


class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control mb-2', 'placeholder':'Email', 'name':'email'}))
    password = forms.CharField(label='Contraseña',widget=forms.PasswordInput(attrs={'class': 'form-control mb-4', 'placeholder':'Contraseña', 'name':'password'}))
                                   
class UserRegisterForm(forms.Form):
    name = forms.CharField(max_length=32, label='Nombre',widget=forms.TextInput(attrs={'class': 'form-control mb-2', 'placeholder':'Nombre', 'name':'name'}))
    last_name = forms.CharField(max_length=32, label='Apellido',widget=forms.TextInput(attrs={'class': 'form-control mb-2', 'placeholder':'Apellido', 'name':'last_name'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control mb-2', 'placeholder':'Email', 'name':'email'}))
    password = forms.CharField(label='Contraseña',widget=forms.PasswordInput(attrs={'class': 'form-control mb-2', 'placeholder':'Contraseña', 'name':'password'}))
    rpassword = forms.CharField(label='Confirmar Contraseña',widget=forms.PasswordInput(attrs={'class': 'form-control mb-4', 'placeholder':'Confirmar Contraseña', 'name':'rpassword'}))
    phoneregex = RegexValidator(regex=r'^\+?58?\d{11,15}$',
        message="El número telefónico debe colocarse en el formato: '+999999999'. Hasta 15 dígitos permitidos.")
    phonenumber = forms.CharField(validators=[phoneregex], max_length=17, label='Teléfono',widget=forms.TextInput(attrs={'class': 'form-control mb-4', 'placeholder':'Teléfono', 'name':'phonenumber'}))

class UserEditForm(forms.Form):
    name = forms.CharField(max_length=32, label='Nombre',widget=forms.TextInput(attrs={'class': 'form-control mb-2', 'placeholder':'Nombre', 'name':'name'}))
    last_name = forms.CharField(max_length=32, label='Apellido',widget=forms.TextInput(attrs={'class': 'form-control mb-2', 'placeholder':'Apellido', 'name':'last_name'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control mb-2', 'placeholder':'Email', 'name':'email'}))
    phoneregex = RegexValidator(regex=r'^\+?58?\d{11,15}$',
        message="El número telefónico debe colocarse en el formato: '+999999999'. Hasta 15 dígitos permitidos.")
    phonenumber = forms.CharField(validators=[phoneregex], max_length=17, label='Teléfono',widget=forms.TextInput(attrs={'class': 'form-control mb-4', 'placeholder':'Teléfono', 'name':'phonenumber'}))

class ChangePasswordForm(forms.Form):
    
    npassword = forms.CharField(label='Contraseña Nueva',widget=forms.PasswordInput(attrs={'class': 'form-control mb-2', 'placeholder':'Contraseña Nueva', 'name':'npassword'}))
    cnpassword = forms.CharField(label='Confirmar Contraseña',widget=forms.PasswordInput(attrs={'class': 'form-control mb-2', 'placeholder':'Confirmar Contraseña', 'name':'cnpassword'}))