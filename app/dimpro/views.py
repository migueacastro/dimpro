from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth import authenticate, login, logout
from .models import User, Order, Product, Order_Product, Client
from .forms import LoginForm, UserRegisterForm
from .decorators import only_for
import json
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
            return render(request, 'dimpro/public/login.html', {
                'form': form
            })
    return render(request, 'dimpro/public/login.html', {
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
                return render(request, 'dimpro/public/login_staff.html', {
                    'message': 'Email o contraseña no valido.', 'form':form
                })
           
            if (user.is_staff and not user.is_superuser):
                login(request, user)
                return HttpResponseRedirect(reverse('dimpro:control'))
            else:
                return render(request, 'dimpro/public/login_staff.html', {
                    'message': 'Email o contraseña no valido.', 'form':form
                })
        else:
            return render(request, 'dimpro/public/login_staff.html', {
                'form': form
            })
    return render(request, 'dimpro/public/login_staff.html', {
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
                return render(request, 'dimpro/public/register.html', {
                    'message': 'Las contraseñas no coinciden.', 'form':form
                })

            if len(password) < 8:
                return render(request, 'dimpro/public/register.html', {
                    'message': 'La contraseña debe tener al menos 8 caracteres.', 'form':form
                })
            
            if email is None or name is None or last_name is None:
                return render(request, 'dimpro/public/register.html', {
                    'message': 'Debe rellenar los campos.', 'form':form
                })
            
            elif not ('@gmail.com' in email or '@outlook.com' in email):
                return render(request, 'dimpro/public/register.html', {
                    'message': 'Email no valido.', 'form':form
                })
            else:
                try:
                    User.objects.get(email=email)
                    return render(request, 'dimpro/public/register.html', {
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
                return render(request, 'dimpro/public/register.html', {
                    'message': 'Usuario ya registrado.', 'form':form
                })
        else:
            return render(request, 'dimpro/public/register.html', {
                'form': form
            })
    return render(request, 'dimpro/public/register.html', {
        'form':UserRegisterForm()
    })

@only_for('anonymous')
def start(request):
    return render(request, 'dimpro/public/start.html')


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
    return render(request, 'dimpro/staff/staff_dashboard.html', {
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
    return render(request, 'dimpro/staff/staff_orders.html', {
        'orders':list_of_orders, 'n_orders': number_of_orders
    })

@only_for('staff')
def staff_clients(request):
    return render(request, 'dimpro/staff/staff_clients.html')

@only_for('staff')
def staff_client_view(request, id):
    seller = User.objects.get(id=id)
    orders = Order.objects.filter(user_email=seller.id).count()

    return render(request, 'dimpro/staff/staff_client_view.html', {
        'seller': seller, 
        'number_of_orders': orders
    })

@only_for('staff')
def staff_order_view(request, id):
    if request.method == "POST":
        pass
    order = Order.objects.get(id=id)
    client = User.objects.get(email=order.user_email)
    return render(request, 'dimpro/staff/staff_order_view.html', {
        'seller': client, 
        'order': order,
        'order_categories': order.product_categories()
    })




@only_for('user')
def index(request):
    return render(request, 'index.html')

def logout_action(request):
    logout(request)
    return render(request, 'dimpro/public/start.html', {
        'message':'Sesión Cerrada'
    })
                  
@only_for('staff')
def list_orders_start(_request):
    orderquery = Order.objects.filter(status='pendiente')
    data = {'orders': []}
    for order in orderquery:
        order_dict = {
            'id': order.id,
            'user_email': f'{order.user_email.name} {order.user_email.last_name}',
            'client_name': order.client_id.name,
            'date': order.date.strftime('%d %B %Y %H:%M'),
            'status': order.status.capitalize(),
            'products': order.product_categories()
        }
        data['orders'].append(order_dict)
    return JsonResponse(data)

@only_for('staff')
def list_orders_all(_request):
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
        }
        data['orders'].append(order_dict)
    return JsonResponse(data)

@only_for('staff')
def list_orders_user(_request, id):
    orderquery = Order.objects.filter(user_email=id)
    data = {'orders': []}
    for order in orderquery:
        order_dict = {
            'id': order.id,
            'user_email': f'{order.user_email.name} {order.user_email.last_name}',
            'client_name': order.client_id.name,
            'date': order.date.strftime('%d %B %Y %H:%M'),
            'status': order.status.capitalize(),
            'products': order.product_categories()
        }
        data['orders'].append(order_dict)
    return JsonResponse(data)

@only_for('staff')
def list_sellers(_request):
    sellerquery = User.objects.filter(is_staff=False, is_superuser=False)
    data = {'sellers': []}
    for user in sellerquery:
        order_dict = {
            'id': user.id,
            'username': f'{user.name} {user.last_name}',
            'date_joined': user.date_joined.strftime('%d %B %Y %H:%M'),
            'last_login': user.last_login.strftime('%d %B %Y %H:%M'),
            'email': user.email,
            'orders': user.user_orders()
        }
        data['sellers'].append(order_dict)
    return JsonResponse(data)

@only_for('staff')
def list_products_for_order(_request, id):
    products = Order_Product.objects.filter(order_id=id)
    data = {'products': []}
    for product in products:
        order_dict = {
            'id': product.product_id.id,
            'name': product.product_id.item,
            'reference': product.product_id.reference,
            'quantity': product.quantity,
            'available-quantity': product.product_id.available_quantity
        }
        data['products'].append(order_dict)
    return JsonResponse(data)

@only_for('staff')
def edit_order(request, id):
    if request.method == 'POST':
            data = json.loads(request.body)
            for row in data:
                quantity = int(row['quantity'])
                try: 
                    product = Product.objects.get(item=row['item'])
                    object = Order_Product.objects.get(order_id=id, product_id=product.id)
                    if quantity == 0:
                        object.delete()
                    else:
                        object.quantity = int(quantity)
                        object.save()
                except Order_Product.DoesNotExist:
                    if quantity == 0:
                        continue
                    else:
                        order = Order.objects.get(id=id)
                        product = Product.objects.get(item=row['item'])
                        Order_Product.objects.create(order_id=order, product_id=product, quantity=quantity)
            return HttpResponseRedirect(reverse('dimpro:control'))
        
    else:
        order = Order.objects.get(id=id)
        products = Product.objects.all()
        return render(request, 'dimpro/staff/staff_order_view_edit.html', {
            'order':order,
            'products': products
        })
    
@only_for('staff')
def list_products(_request):
    products = Product.objects.all()
    data = {'products': []}
    for product in products:
        if product.available_quantity <= 0:
            continue
        if product.reference == '':
            continue
        product_dict = {
            'id': product.id,
            'item': product.item,
            'details': product.details,
            'reference': product.reference,
            'available_quantity': product.available_quantity
        }
        data['products'].append(product_dict)
    return JsonResponse(data)