from django import forms

class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control mb-2', 'placeholder':'Email', 'name':'email'}))
    password = forms.CharField(label='Contraseña',widget=forms.PasswordInput(attrs={'class': 'form-control mb-4', 'placeholder':'Contraseña', 'name':'password'}))
                                   
class UserRegisterForm(forms.Form):
    name = forms.CharField(max_length=32, label='Nombre',widget=forms.TextInput(attrs={'class': 'form-control mb-2', 'placeholder':'Nombre', 'name':'name'}))
    last_name = forms.CharField(max_length=32, label='Apellido',widget=forms.TextInput(attrs={'class': 'form-control mb-2', 'placeholder':'Apellido', 'name':'last_name'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control mb-2', 'placeholder':'Email', 'name':'email'}))
    password = forms.CharField(label='Contraseña',widget=forms.PasswordInput(attrs={'class': 'form-control mb-2', 'placeholder':'Contraseña', 'name':'password'}))
    rpassword = forms.CharField(label='Confirmar Contraseña',widget=forms.PasswordInput(attrs={'class': 'form-control mb-4', 'placeholder':'Confirmar Contraseña', 'name':'rpassword'}))