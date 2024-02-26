from django.shortcuts import render
from django.core.cache import cache
from django.urls import reverse
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import check_password, make_password
from .models import User, Order, Product, Order_Product, Contact, AlegraUser
from .forms import LoginForm, UserRegisterForm, UserEditForm, ChangePasswordForm, AlegraUserForm, CheckOperatorPasswordForm
from .decorators import only_for
from dimpro.management.commands.updatedb import update
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
                return HttpResponseRedirect(reverse('dimpro:index'))
            else:
                return render(request, 'dimpro/public/login.html', {
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
            user = authenticate(request, username=email, password=password)
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return render(request, 'dimpro/public/login_staff.html', {
                    'message': 'Email o contraseña no valido.', 'form':form
                })
            if user is not None:
                if (user.is_staff and not user.is_superuser):
                    login(request, user)
                    return HttpResponseRedirect(reverse('dimpro:control'))
                else:
                    return render(request, 'dimpro/public/login_staff.html', {
                        'message': 'Email o contraseña no valido.', 'form':form
                    })
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
            phonenumber = form.cleaned_data['phonenumber']
            if password != rpassword:
                return render(request, 'dimpro/public/register.html', {
                    'message': 'Las contraseñas no coinciden.', 'form':form
                })

            if len(password) < 8:
                return render(request, 'dimpro/public/register.html', {
                    'message': 'La contraseña debe tener al menos 8 caracteres.', 'form':form
                })
            
            if not any(c.isalpha() for c in password):
                return render(request, 'dimpro/public/register.html', {
                    'message': 'La contraseña debe contener letras del alfabeto.', 'form':form
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
                User.objects.create_user(name=name, last_name=last_name, email=email, password=password, phonenumber=phonenumber)
                user = authenticate(request, username=email, password=password)
                login(request, user)
                messages.success(request, 'Usuario registrado exitosamente.')
                return HttpResponseRedirect(reverse('dimpro:index'))
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



def logout_action(request):
    logout(request)
    messages.info(request, 'Sesión cerrada.')
    return render(request, 'dimpro/public/start.html', {
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

@only_for('signedin')
def list_orders_user(_request, id):
    user = User.objects.get(id=id)
    if (user.is_staff):
        return HttpResponseRedirect(reverse('dimpro:index'))
    orderquery = Order.objects.filter(user_email=user.id)
    data = {'orders': []}
    for order in orderquery:
        order_dict = {
            'id': order.id,
            'user_email': f'{user.email} {user.last_name}',
            'client_name': order.client_id.name,
            'date': order.date.strftime('%d %B %Y %H:%M'),
            'status': order.status.capitalize(),
            'products': order.product_categories(),
            'total': order.total
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
            'phonenumber': user.phonenumber,
            'orders': user.user_orders()
        }
        data['sellers'].append(order_dict)
    return JsonResponse(data)

@only_for('signedin')
def list_products_for_order(_request, id):
    products = Order_Product.objects.filter(order_id=id)

    data = {'products': []}
    for product in products:
        order_dict = {
            'id': product.product_id.id,
            'name': product.product_id.item,
            'reference': product.product_id.reference,
            'quantity': product.quantity,
            'available-quantity': product.product_id.available_quantity,
            'price': product.price,
            'cost': product.cost
        }
        data['products'].append(order_dict)
    return JsonResponse(data)

@only_for('staff')
def edit_order(request, id):
    if request.method == 'POST':
        try:
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
           
        except Exception:
            total = request.POST.get('total-tosubmit')
            order = Order.objects.get(id=id)
            type = request.POST.get('order-type').lower()
            order.total = total
            order.type = type
            order.save()
        messages.success(request, 'Pedido actualizado exitosamente.')
        return HttpResponseRedirect(f'/app/staff/view/order/{id}')

    else:
        order = Order.objects.get(id=id)
        products = Product.objects.all()
        return render(request, 'dimpro/staff/staff_order_view_edit.html', {
            'order':order,
            'products': products
        })
    
@only_for('signedin')
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
            'price': product.price,
            'available_quantity': product.available_quantity
        }
        data['products'].append(product_dict)
    return JsonResponse(data)

@only_for('staff')
def staff_profile(request,id):
    # AUTH
    user = request.user
    if request.user.id != id:
        return HttpResponseRedirect(f'/app/staff/profile/{request.user.id}/')
    return render(request, 'dimpro/staff/staff_profile.html')


@only_for('signedin')
def staff_profile_edit(request, id):
    user = request.user
    if request.user.id != id:
        return HttpResponseRedirect(f'/app/staff/profile/{request.user.id}/')
    if request.method == 'POST':
        form = UserEditForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            phonenumber = form.cleaned_data['phonenumber']

            if email is None or name is None or last_name is None:
                return render(request, 'dimpro/staff/staff_profile_edit.html', {
                    'message': 'Debe rellenar los campos.', 'form':form
                })
            
            elif not ('@gmail.com' in email or '@outlook.com' in email):
                return render(request, 'dimpro/staff/staff_profile_edit.html', {
                    'message': 'Email no valido.', 'form':form
                })
            else:
                try:
                    registered_user = User.objects.get(email=email)
                    if registered_user.id != id:
                        return render(request, 'dimpro/staff/staff_profile_edit.html', {
                        'message': 'Usuario ya registrado.', 'form':form
                })
                except User.DoesNotExist:
                    pass
            user_to_edit = User.objects.get(id=id)
            user_to_edit.name = name
            user_to_edit.last_name = last_name
            user_to_edit.email = email
            user_to_edit.phonenumber = phonenumber
            user_to_edit.save()
            messages.success(request, 'Perfil editado exitosamente.')
            return HttpResponseRedirect(f'/app/staff/profile/{id}/')
        else:
            return render(request, 'dimpro/staff/staff_profile_edit.html', {
                'form': form
            })
    user = request.user
    data = {'name': request.user.name, 
            'last_name': request.user.last_name,
            'email': request.user.email,
            'phonenumber': request.user.phonenumber}
    return render(request, 'dimpro/staff/staff_profile_edit.html', {
        'user':user, 
        'form':UserEditForm(data=data)})

@only_for('signedin')
def staff_changepw(request, id):
    user = request.user
    if request.user.id != id:
        return HttpResponseRedirect(f'/app/staff/profile/{request.user.id}/')
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            
            usertocheck = User.objects.get(id=request.user.id)
            opassword = form.cleaned_data['opassword']
            npassword = form.cleaned_data['npassword']
            cnpassword = form.cleaned_data['cnpassword']

            if not usertocheck.check_password(opassword):
                return render(request, 'dimpro/staff/staff_register.html', {
                    'message': 'Contraseña incorrecta.', 'form':form
                })
            if npassword != cnpassword:
                return  render(request, 'dimpro/staff/staff_changepw.html', {
                'message': 'Las nuevas contraseñas deben ser iguales.',
                 'form': form
            })

            if len(npassword) < 8:
                return render(request, 'dimpro/staff/staff_register.html', {
                    'message': 'La contraseña debe tener al menos 8 caracteres.', 'form':form
                })
            if not any(c.isalpha() for c in npassword):
                return render(request, 'dimpro/staff/staff_register.html', {
                    'message': 'La contraseña debe contener letras del alfabeto.', 'form':form
                })
            nuser = User.objects.get(email=user.email) 
            
            nuser.set_password(npassword)
            nuser.save()
            newuser = authenticate(request,username=user.email, password=npassword)
            login(request, newuser)
            messages.success(request, 'Contraseña actualizada exitosamente.')
            return HttpResponseRedirect(f'/app/staff/profile/{id}/')
        else:
            return render(request, 'dimpro/staff/staff_changepw.html', {
                'form': form
            })
    return render(request, 'dimpro/staff/staff_changepw.html', {
        'user':user,
        'form':ChangePasswordForm()
    })


@only_for('operator')
def delete_user(request, id):
    user = User.objects.get(id=id)
    user.delete()
    messages.success(request, 'Usuario eliminado exitosamente.')
    return HttpResponseRedirect(reverse('dimpro:staff_settings'))

@only_for('operator')
def staff_settings(request):
    return render(request, 'dimpro/staff/staff_settings.html')

@only_for('operator')
def list_employees(_request):
    employeequery = User.objects.filter(is_staff=True, is_superuser=False).exclude(is_operator=True)
    data = {'employees': []}
    for user in employeequery:
        date_joined = user.date_joined.strftime('%d %B %Y %H:%M') if user.date_joined else 'No se ha unido aún'
        last_login = user.last_login.strftime('%d %B %Y %H:%M') if user.last_login else 'No ha iniciado sesión aún'
        order_dict = {
            'id': user.id,
            'username': f'{user.name} {user.last_name}',
            'date_joined': date_joined,
            'last_login': last_login,
            'email': user.email,
            'phonenumber': user.phonenumber,
            'orders': user.user_orders()
        }
        data['employees'].append(order_dict)
    return JsonResponse(data)

@only_for('operator')
def staff_employees(request):
    return render(request, 'dimpro/staff/staff_employees.html')

@only_for('operator')
def staff_register_employee(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            rpassword = form.cleaned_data['rpassword']
            phonenumber = form.cleaned_data['phonenumber']
            if password != rpassword:
                return render(request, 'dimpro/staff/staff_register.html', {
                    'message': 'Las contraseñas no coinciden.', 'form':form
                })

            if len(password) < 8:
                return render(request, 'dimpro/staff/staff_register.html', {
                    'message': 'La contraseña debe tener al menos 8 caracteres.', 'form':form
                })
            if not any(c.isaplha() for c in password):
                return render(request, 'dimpro/staff/staff_register.html', {
                    'message': 'La contraseña debe contener letras del alfabeto.', 'form':form
                })
            if email is None or name is None or last_name is None:
                return render(request, 'dimpro/staff/staff_register.html', {
                    'message': 'Debe rellenar los campos.', 'form':form
                })
            
            elif not ('@gmail.com' in email or '@outlook.com' in email):
                return render(request, 'dimpro/staff/staff_register.html', {
                    'message': 'Email no valido.', 'form':form
                })
            else:
                try:
                    User.objects.get(email=email)
                    return render(request, 'dimpro/staff/staff_register.html', {
                    'message': 'Usuario ya registrado.', 'form':form
                })
                
                except User.DoesNotExist:
                    pass
                
            user = authenticate(request, username=email, password=password)
            if user is None:
                User.objects.create_staff(name=name, last_name=last_name, email=email, password=password, phonenumber=phonenumber)
                messages.success(request, 'Usuario registrado exitosamente.')
                return HttpResponseRedirect(reverse('dimpro:staff_employees'))
            else:
                return render(request, 'dimpro/staff/staff_register.html', {
                    'message': 'Usuario ya registrado.', 'form':form
                })
        else:
            return render(request, 'dimpro/staff/staff_register.html', {
                'form': form
            })
    return render(request, 'dimpro/staff/staff_register.html', {
        'form': UserRegisterForm()
    })

@only_for('operator')
def staff_changetk(request):
    account = AlegraUser.objects.get(id=1)
    if request.method == 'POST':
        form = AlegraUserForm(request.POST)
        if form.is_valid():
            account.email = form.cleaned_data['email']
            account.token = form.cleaned_data['token']
            account.save()
            messages.info(request, 'Token de Alegra actualizado.')
            return HttpResponseRedirect(reverse('dimpro:staff_settings'))
        else:
            return render(request, 'dimpro/staff/staff_changetk.html', {
            'form': form})
    data = {'email':account.email, 'token':account.token}
    return render(request, 'dimpro/staff/staff_changetk.html', {
        'form': AlegraUserForm(data=data)
    })

@only_for('operator')
def staff_updatedb(request):
    update()
    messages.info(request, 'La base de datos ha sido actualizada.')
    return HttpResponseRedirect(reverse('dimpro:staff_settings'))

@only_for('staff')
def staff_changestatus(request, id):
    order = Order.objects.get(id=id)
    if order.status == 'pendiente':
        order.status = 'preparado'
        order.save()
    else:
        order.status = 'pendiente'
        order.save()
    messages.success(request, 'Estatus cambiado exitosamente')
    return HttpResponseRedirect(f'/app/staff/view/order/{order.id}')

@only_for('user')
def index(request):
    user = request.user
    return render(request, 'dimpro/client/client_dashboard.html',{
        'user': user})

@only_for('user')
def client_profile(request,id):
    # AUTH
    user = request.user
    if request.user.id != id:
        return HttpResponseRedirect(f'/app/client/profile/{request.user.id}/')
    return render(request, 'dimpro/client/client_profile.html')


@only_for('user')
def client_orders(request, id):
    user = request.user
    
    try:
        list_of_orders = Order.objects.filter(user_email=id)
        number_of_orders = list_of_orders.count()
    except Order.DoesNotExist:
        list_of_orders = []
        number_of_orders = 0
    except User.DoesNotExist:
        number_of_sellers = 0
    return render(request, 'dimpro/client/client_orders.html', {
        'user': user, 'orders':list_of_orders, 'n_orders': number_of_orders
    })

@only_for('user')
def client_orders_add(request, id):
    if id != request.user.id: 
        return HttpResponseRedirect(reverse('dimpro:index'))
    
    if request.method == 'POST':
        user_id = User.objects.get(id = request.POST.get('user_id'))                   
        client_id = Contact.objects.get(name = request.POST.get('client_id'))

        status = 'pendiente'

        new_order = Order.objects.create(user_email=user_id, client_id = client_id, status='pendiente', type='factura')
        new_order.save(force_update=True)
        return HttpResponseRedirect(f'/app/client/order/edit/{new_order.id}/')

    user = request.user
    list_of_clients = Contact.objects.all()
    return render(request, 'dimpro/client/client_create_order.html', {
        'clients': list_of_clients, 'user':user})


@only_for('user')
def client_orders_edit(request, id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            for row in data:
                quantity = int(row['quantity'])
                cost = float(row['cost'])
                try: 
                    product = Product.objects.get(item=row['item'])
                    object = Order_Product.objects.get(order_id=id, product_id=product.id)
                    if quantity == 0:
                        object.delete()
                    else:
                        object.quantity = int(quantity)
                        object.cost = cost
                        object.save()
                except Order_Product.DoesNotExist:
                    if quantity == 0:
                        continue
                    else:
                        order = Order.objects.get(id=id)
                        product = Product.objects.get(item=row['item'])
                        new_product = Order_Product.objects.create(order_id=order, product_id=product, quantity=quantity, cost=cost)
                        new_product.save(force_update=True)
        except Exception:
            total = request.POST.get('total-tosubmit')
            type = request.POST.get('order-type').lower()
            order = Order.objects.get(id=id)
            order.total = total
            order.type = type
            order.save()
                    
        messages.success(request, 'Pedido actualizado exitosamente.')
        return HttpResponseRedirect(f'/app/client/order/view/{id}/')
        
    else:
        order = Order.objects.get(id=id)
        products = Product.objects.all()
        return render(request, 'dimpro/client/client_edit_order.html', {
            'order':order,
            'products': products
        })
    

@only_for('user')
def client_order_view(request, id):
    if request.method == "POST":
        pass
    order = Order.objects.get(id=id)
    client = User.objects.get(email=order.user_email)
    return render(request, 'dimpro/client/client_order_view.html', {
        'seller': client, 
        'order': order,
        'client': order.client_id.name,
        'order_categories': order.product_categories()
    })

@only_for('user')
def client_order_delete(request, id):
    order = Order.objects.get(id=id)
    if order.status == 'preparado':
        messages.error(request, 'No se puede eliminar un pedido preparado.')
        return HttpResponseRedirect(f'/app/client/orders/{order.user_email.id}/')
    if request.user.id != order.user_email.id:
        return HttpResponseRedirect(reverse('dimpro:index'))
    
    order.delete()
    messages.success(request,'Pedido eliminado exitosamente.')
    return HttpResponseRedirect(f'/app/client/orders/{order.user_email.id}/')


@only_for('operator')
def staff_order_delete(request, id):
    order = Order.objects.get(id=id)
    order.delete()
    messages.success(request,'Pedido eliminado exitosamente.')
    return HttpResponseRedirect(f'/app/client/orders/{order.user_email.id}/')


@only_for('staff')
def list_contacts_all(_request):
    contacts = Contact.objects.all()
    data = {'contacts': []}
    for contact in contacts:
        contact_dict = {
            'name': contact.id,
        }
        data['contacts'].append(contact_dict)
    return JsonResponse(data)

@only_for('operator')
def verify_password(request):
    user = request.user
    if request.method == 'POST':
        form = CheckOperatorPasswordForm(request.POST)
        usertocheck = User.objects.get(id=user.id)
        
        if form.is_valid():
            password = form.cleaned_data['password']
            if usertocheck.check_password(password):
                return HttpResponseRedirect(reverse('dimpro:staff_changetk'))
            else:
                return render(request, 'dimpro/staff/staff_authenticate.html', {
                    'user': request.user,
                    'message': 'Contraseña incorrecta.',
                    'form': form
                })
        return render(request, 'dimpro/staff/staff_authenticate.html', {
                    'user': request.user,
                    'form': form
                })
    return render(request, 'dimpro/staff/staff_authenticate.html', {
        'user': request.user,
        'form': CheckOperatorPasswordForm()
    })