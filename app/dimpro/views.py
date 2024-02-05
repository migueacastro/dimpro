from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from .models import User
from .forms import LoginForm, UserRegisterForm
from .decorators import only_for
# Create your views here.

@only_for('anonymous')
def login_user(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, username=email, password=password)
            if user is not None and not user.is_staff and not user.is_superuser:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return render(request, 'dimpro/login.html', {
                    'message': 'Email o contraseña no valido.', 'form':form
                })
        else:
            return render(request, 'dimpro/login.html', {
                'form': form
            })
    return render(request, 'dimpro/login.html', {
        'form': LoginForm()
    })

@only_for('anonymous')
def login_staff(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, username=email, password=password)
            if user is not None and user.is_staff and not user.is_superuser:
                login(request, user)
                return HttpResponseRedirect(reverse('control'))
            else:
                return render(request, 'dimpro/login_staff.html', {
                    'message': 'Email o contraseña no valido.', 'form':form
                })
        else:
            return render(request, 'dimpro/login_staff.html', {
                'form': form
            })
    return render(request, 'dimpro/login_staff.html', {
        'form':LoginForm()
    })

@only_for('anonymous')
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            rpassword = form.cleaned_data['rpassword']

            if password != rpassword:
                return render(request, 'dimpro/register.html', {
                    'message': 'Las contraseñas no coinciden.', 'form':form
                })

            if len(password) < 8:
                return render(request, 'dimpro/register.html', {
                    'message': 'La contraseña debe tener al menos 8 caracteres.', 'form':form
                })
            
            if email is None or name is None or last_name is None:
                return render(request, 'dimpro/register.html', {
                    'message': 'Debe rellenar los campos.', 'form':form
                })
            
            elif not ('@gmail.com' in email or '@outlook.com' in email):
                return render(request, 'dimpro/register.html', {
                    'message': 'Email no valido.', 'form':form
                })
            else:
                try:
                    User.objects.get(email=email)
                    return render(request, 'dimpro/register.html', {
                    'message': 'Usuario ya registrado.', 'form':form
                })
                
                except User.DoesNotExist:
                    pass
                
            user = authenticate(request, username=email, password=password)
            if user is None:
                User.objects.create_user(name=name, last_name=last_name, email=email, password=password)
                user = authenticate(request, username=email, password=password)
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return render(request, 'dimpro/register.html', {
                    'message': 'Usuario ya registrado.', 'form':form
                })
        else:
            return render(request, 'dimpro/register.html', {
                'form': form
            })
    return render(request, 'dimpro/register.html', {
        'form':UserRegisterForm()
    })

@only_for('anonymous')
def start(request):
    return render(request, 'dimpro/start.html')


@only_for('staff')
def control(request):
    pass


@only_for('user')
def index(request):
    return render(request, 'index.html')

def logout_action(request):
    logout(request)
    return render(request, 'dimpro/start.html', {
        'message':'Sesión Cerrada'
    })
                  