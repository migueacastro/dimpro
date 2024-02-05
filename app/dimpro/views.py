from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from .models import User
# Create your views here.




def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('start'))
    if not request.user.is_staff and not request.user.is_superuser:
        return render(request, 'index.html')
    
    
def start(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('index'))
    return render(request, 'dimpro/start.html')

def login_user(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('index'))
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)
        if (user is not None) and (not user.is_staff) and (not user.is_superuser):
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, 'dimpro/login.html', {
                'message': 'Email o contraseña no valido.'
            })
    return render(request, 'dimpro/login.html')

def login_staff(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('index'))
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)
        if (user is not None) and (user.is_staff) and (not user.is_superuser):
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, 'dimpro/login.html', {
                'message': 'Email o contraseña no valido.'
            })
    return render(request, 'dimpro/login_staff.html')

def register(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('index'))
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        rpassword = request.POST['rpassword']

        if password != rpassword:
            return render(request, 'dimpro/register.html', {
                'message': 'Las contraseñas no coinciden.'
            })

        if len(password) < 8:
            return render(request, 'dimpro/register.html', {
                'message': 'La contraseña debe tener al menos 8 caracteres.'
            })
        
        if email is None or name is None:
            return render(request, 'dimpro/register.html', {
                'message': 'Debe rellenar los campos.'
            })
        
        elif not ('@gmail.com' in email or '@outlook.com' in email):
            return render(request, 'dimpro/register.html', {
                'message': 'Email no valido.'
            })
        else:
            try:
                User.objects.get(email=email)
                return render(request, 'dimpro/register.html', {
                'message': 'Usuario ya registrado.'
            })
            
            except User.DoesNotExist:
                pass
            
        user = authenticate(request, username=email, password=password)
        if user is None:
            User.objects.create_user(name=name, email=email, password=password)
            user = authenticate(request, username=email, password=password)
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, 'dimpro/register.html', {
                'message': 'Usuario ya registrado.'
            })
    return render(request, 'dimpro/register.html')