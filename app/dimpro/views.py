from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth import authenticate, login, logout
from .models import User, Order, Product, Order_Product, Client
from .forms import LoginForm, UserRegisterForm
from .decorators import only_for
from .tables import order_table, client_table, client_orders_table
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
            try:
                user = User.objects.get(email=email, password=password)
            except User.DoesNotExist:
                return render(request, 'dimpro/login_staff.html', {
                    'message': 'Email o contraseña no valido.', 'form':form
                })
           
            if (user.is_staff and not user.is_superuser):
                login(request, user)
                return HttpResponseRedirect(reverse('dimpro:control'))
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

    user = request.user
    
    try:
        list_of_orders = Order.objects.filter()
        number_of_orders = list_of_orders.count()
        number_of_sellers = User.objects.filter(is_staff=False, is_superuser=False).count()
    except Order.DoesNotExist:
        list_of_orders = []
        number_of_orders = 0
    except User.DoesNotExist:
        number_of_sellers = 0
    return render(request, 'dimpro/staff_dashboard.html', {
        'user': user, 'orders':list_of_orders, 'n_orders': number_of_orders, 'n_sellers':number_of_sellers
    })

@only_for('staff')
def staff_orders(request):
    try:
        list_of_orders = Order.objects.filter()
        number_of_orders = list_of_orders.count()
    except Order.DoesNotExist:
        list_of_orders = []
        number_of_orders = 0
    return render(request, 'dimpro/staff_orders.html', {
        'orders':list_of_orders, 'n_orders': number_of_orders, 'order_table': order_table()
    })

@only_for('staff')
def staff_clients(request):
    return render(request, 'dimpro/staff_clients.html', {
        'client_table': client_table()
    })

@only_for('staff')
def staff_client_view(request, id):
    client = User.objects.get(id=id)
    orders = Order.objects.filter(user_email=client.id).count()

    return render(request, 'dimpro/staff_client_view.html', {
        'client': client, 
        'number_of_orders': orders,
        'client_orders_table': client_orders_table(client.id) 
    })

@only_for('staff')
def staff_order_view(request, id):
    if request.method == "POST":
        pass
    order = Order.objects.get(id=id)
    product = Product.objects.get(id=order.product_id.id)
    client = User.objects.get(email=order.user_email)
    return render(request, 'dimpro/staff_order_view.html', {
        'client': client, 
        'order': order,
        'product': product
    })




@only_for('user')
def index(request):
    return render(request, 'index.html')

def logout_action(request):
    logout(request)
    return render(request, 'dimpro/start.html', {
        'message':'Sesión Cerrada'
    })
                  
@only_for('staff')
def list_orders(_request):
    orderquery = Order.objects.all()
    data = {'orders': []}
    for order in orderquery:
        order_dict = {
            'id': order.id,
            'user_email': f'{order.user_email.name} {order.user_email.last_name}',
            'client_name': order.client_id.name,
            'date': order.date.strftime('%d %B %Y %H:%M'),
            'status': order.status.capitalize(),
            'products': order.product_categories()
            # include other fields here
        }
        data['orders'].append(order_dict)
    return JsonResponse(data)