from django.shortcuts import render
from django.template import RequestContext
from django.urls import reverse
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.conf import settings

from django.contrib.auth import authenticate, login, logout
from django.contrib.staticfiles import finders
from .models import User, Order, Product, Order_Product, Contact, AlegraUser, PriceType, Note
from .forms import (
    LoginForm,
    UserRegisterForm,
    UserEditForm,
    ChangePasswordForm,
    AlegraUserForm,
    CheckOperatorPasswordForm,
)
from .decorators import only_for
from dimpro.management.commands import updatedb
import json


# For pdf exporting
from django.http import FileResponse
import io
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.lib.pagesizes import letter
from reportlab.platypus import BaseDocTemplate, PageTemplate, Frame, Table, Paragraph, Spacer, Image, TableStyle
from svglib.svglib import svg2rlg
from reportlab.lib.styles import getSampleStyleSheet

# For webpush
from django.views.decorators.csrf import csrf_exempt
from webpush import send_user_notification
from django.shortcuts import get_object_or_404
from django.conf import settings


webpush_settings = getattr(settings, 'WEBPUSH_SETTINGS', {})
vapid_key = webpush_settings.get('VAPID_PUBLIC_KEY')

# Get styles for cells in table prints
styles = getSampleStyleSheet()


# Sending emails
from django.core.mail import EmailMessage
from django.conf import settings


# Create your views here.


def error404(request, exception):
    return render(request, 'dimpro/public/404.html', status=404)
    
def error500(request):
    
    return render(request, 'dimpro/public/500.html', status=500)

@only_for("anonymous")
def login_user(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=email, password=password)
            if user is not None and not user.is_staff and not user.is_superuser:
                if user.check_password(password):
                    login(request, user)
                    return HttpResponseRedirect(reverse("dimpro:index"))
                else:
                    return render(
                        request,
                        "dimpro/public/login.html",
                        {"message": "Email o contraseña no valido.", "form": form},
                    )
            else:
                return render(
                    request,
                    "dimpro/public/login.html",
                    {"message": "Email o contraseña no valido.", "form": form},
                )
        else:
            return render(request, "dimpro/public/login.html", {"form": form})
    return render(request, "dimpro/public/login.html", {"form": LoginForm()})


@only_for("anonymous")
def login_staff(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=email, password=password)
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return render(
                    request,
                    "dimpro/public/login_staff.html",
                    {"message": "Email o contraseña no valido.", "form": form},
                )
            if user is not None:
                if user.is_staff and not user.is_superuser:
                    if user.check_password(password):
                        login(request, user)
                        return HttpResponseRedirect(reverse("dimpro:control"))
                    else:
                        return render(
                            request,
                            "dimpro/public/login_staff.html",
                            {"message": "Email o contraseña no valido.", "form": form},
                        )
                else:
                    return render(
                        request,
                        "dimpro/public/login_staff.html",
                        {"message": "Email o contraseña no valido.", "form": form},
                    )
            return render(
                request,
                "dimpro/public/login_staff.html",
                {"message": "Email o contraseña no valido.", "form": form},
            )
        else:
            return render(request, "dimpro/public/login_staff.html", {"form": form})
    return render(request, "dimpro/public/login_staff.html", {"form": LoginForm()})


@only_for("anonymous")
def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            last_name = form.cleaned_data["last_name"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            rpassword = form.cleaned_data["rpassword"]
            phonenumber = form.cleaned_data["phonenumber"]
            if password != rpassword:
                return render(
                    request,
                    "dimpro/public/register.html",
                    {"message": "Las contraseñas no coinciden.", "form": form},
                )

            if len(password) < 8:
                return render(
                    request,
                    "dimpro/public/register.html",
                    {
                        "message": "La contraseña debe tener al menos 8 caracteres.",
                        "form": form,
                    },
                )

            if not any(c.isalpha() for c in password):
                return render(
                    request,
                    "dimpro/public/register.html",
                    {
                        "message": "La contraseña debe contener letras del alfabeto.",
                        "form": form,
                    },
                )

            if email is None or name is None or last_name is None:
                return render(
                    request,
                    "dimpro/public/register.html",
                    {"message": "Debe rellenar los campos.", "form": form},
                )

            elif not ("@gmail.com" in email or "@outlook.com" in email):
                return render(
                    request,
                    "dimpro/public/register.html",
                    {"message": "Email no valido.", "form": form},
                )
            else:
                try:
                    User.objects.get(email=email)
                    return render(
                        request,
                        "dimpro/public/register.html",
                        {"message": "Usuario ya registrado.", "form": form},
                    )

                except User.DoesNotExist:
                    pass

            user = authenticate(request, username=email, password=password)
            if user is None:
                User.objects.create_user(
                    name=name,
                    last_name=last_name,
                    email=email,
                    password=password,
                    phonenumber=phonenumber,
                )
                user = authenticate(request, username=email, password=password)
                login(request, user)
                messages.success(request, "Usuario registrado exitosamente.")
                return HttpResponseRedirect(reverse("dimpro:index"))
            else:
                return render(
                    request,
                    "dimpro/public/register.html",
                    {"message": "Usuario ya registrado.", "form": form},
                )
        else:
            return render(request, "dimpro/public/register.html", {"form": form})
    return render(request, "dimpro/public/register.html", {"form": UserRegisterForm()})


@only_for("anonymous")
def start(request):
    return render(request, "dimpro/public/start.html")


@only_for("staff")
def control(request):
    user = request.user

    try:
        list_of_orders = Order.objects.filter()
        number_of_orders = list_of_orders.count()
        number_of_sellers = User.objects.filter(
            is_staff=False, is_superuser=False
        ).count()
    except Order.DoesNotExist:
        list_of_orders = []
        number_of_orders = 0
    except User.DoesNotExist:
        number_of_sellers = 0
    return render(
        request,
        "dimpro/staff/staff_dashboard.html",
        {
            "vapid_key":vapid_key,
            "user": user,
            "orders": list_of_orders,
            "n_orders": number_of_orders,
            "n_sellers": number_of_sellers,
        },
    )


@only_for("staff")
def staff_orders(request):
    try:
        list_of_orders = Order.objects.filter()
        number_of_orders = list_of_orders.count()
    except Order.DoesNotExist:
        list_of_orders = []
        number_of_orders = 0
    return render(
        request,
        "dimpro/staff/staff_orders.html",
        {"orders": list_of_orders, "n_orders": number_of_orders},
    )


@only_for("staff")
def staff_clients(request):
    return render(request, "dimpro/staff/staff_clients.html")


@only_for("staff")
def staff_client_view(request, id):
    seller = User.objects.get(id=id)
    orders = Order.objects.filter(user_email=seller.id).count()

    return render(
        request,
        "dimpro/staff/staff_client_view.html",
        {"seller": seller, "number_of_orders": orders},
    )


@only_for("staff")
def staff_order_view(request, id):
    if request.method == "POST":
        pass
    order = Order.objects.get(id=id)
    client = User.objects.get(email=order.user_email)
    return render(
        request,
        "dimpro/staff/staff_order_view.html",
        {
            "seller": client,
            "order": order,
            "order_categories": order.product_categories(),
        },
    )


def logout_action(request):
    logout(request)
    messages.info(request, "Sesión cerrada.")
    return render(request, "dimpro/public/start.html", {'logout': True})


@only_for("staff")
def list_orders_start(_request):
    orderquery = Order.objects.filter(status="pendiente").order_by("-date")
    data = {"orders": []}
    for order in orderquery:
        order_dict = {
            "id": order.id,
            "user_email": f"{order.user_email.name} {order.user_email.last_name}",
            "client_name": order.client_id.name,
            "date": order.date.strftime("%d %B %Y %H:%M"),
            "status": order.status.capitalize(),
            "products": order.product_categories(),
        }
        data["orders"].append(order_dict)
    return JsonResponse(data)


@only_for("staff")
def list_orders_all(_request):
    orderquery = Order.objects.all().order_by("-date")
    data = {"orders": []}
    for order in orderquery:
        order_dict = {
            "id": order.id,
            "user_email": f"{order.user_email.name} {order.user_email.last_name}",
            "client_name": order.client_id.name,
            "date": order.date.strftime("%d %B %Y %H:%M"),
            "status": order.status.capitalize(),
            "products": order.product_categories(),
        }
        data["orders"].append(order_dict)
    return JsonResponse(data)


@only_for("signedin")
def list_orders_user(_request, id):
    user = User.objects.get(id=id)
    if user.is_staff:
        return HttpResponseRedirect(reverse("dimpro:index"))
    orderquery = Order.objects.filter(user_email=user.id).order_by("-date")
    data = {"orders": []}
    for order in orderquery:
        order_dict = {
            "id": order.id,
            "user_email": f"{user.email}",
            "client_name": order.client_id.name,
            "date": order.date.strftime("%d %B %Y %H:%M"),
            "status": order.status.capitalize(),
            "products": order.product_categories(),
            "total": order.total,
        }
        data["orders"].append(order_dict)
    return JsonResponse(data)


@only_for("staff")
def list_sellers(_request):
    sellerquery = User.objects.filter(is_staff=False, is_superuser=False)
    data = {"sellers": []}
    for user in sellerquery:
        order_dict = {
            "id": user.id,
            "username": f"{user.name} {user.last_name}",
            "date_joined": user.date_joined.strftime("%d %B %Y %H:%M"),
            "last_login": user.last_login.strftime("%d %B %Y %H:%M"),
            "email": user.email,
            "phonenumber": user.phonenumber,
            "orders": user.user_orders(),
        }
        data["sellers"].append(order_dict)
    return JsonResponse(data)


@only_for("signedin")
def list_products_for_order(_request, id):
    products = Order_Product.objects.filter(order_id=id)

    data = {"products": []}
    for product in products:
        order_dict = {
            "id": product.product_id.id,
            "name": product.product_id.item,
            "reference": product.product_id.reference,
            "quantity": product.quantity,
            "available-quantity": product.product_id.available_quantity,
            "price": product.price,
            "cost": product.cost,
        }
        data["products"].append(order_dict)
    return JsonResponse(data)


@only_for("staff")
def edit_order(request, id):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            for product in Order_Product.objects.filter(order_id=Order.objects.get(id=id)):
                product.delete()
            
            for row in data:
                quantity = int(row["quantity"])
                cost = float(row["cost"])
                order = Order.objects.get(id=id)
                product = Product.objects.filter(item=row["item"]).order_by("id").first()
                price = float(row["price"])

                if quantity <= 0:
                    continue
                else:
                    
                    new_product = Order_Product.objects.create(
                        order_id=order,
                        product_id=product,
                        quantity=quantity,
                        cost=cost,
                        price=price,
                    )
                    new_product.save(force_update=True)

        except Exception:
            total = request.POST.get("total-tosubmit")
            pricetype = request.POST.get("price-tosubmit")
            order = Order.objects.get(id=id)
            type = request.POST.get("order-type").lower()
            order.pricetype = pricetype
            order.total = total
            order.type = type
            order.save()
        messages.success(request, "Pedido actualizado exitosamente.")
        return HttpResponseRedirect(f"/staff/view/order/{id}")

    else:
        order = Order.objects.get(id=id)
        products = Product.objects.filter(price__gt=0)
        pricetypes = PriceType.objects.all()
        try:
            percentage = PriceType.objects.get(name = order.pricetype).percentage
        except PriceType.DoesNotExist:
            percentage = 0
        return render(
            request,
            "dimpro/staff/staff_order_view_edit.html",
            {"order": order, "products": products, "pricetypes": pricetypes, "percentage": percentage, "note":Note.objects.get(name = "ADVERTENCIA")},
        )


@only_for("signedin")
def list_products(_request):
    products = Product.objects.filter(price__gt=0)
    data = {"products": []}
    for product in products:
        if product.available_quantity <= 0 or product.reference == "":
            continue
        product_dict = {
            "id": product.id,
            "item": product.item,
            "details": product.details,
            "reference": product.reference,
            "price": product.price,
            "available_quantity": product.available_quantity,
        }
        data["products"].append(product_dict)
    return JsonResponse(data)


@only_for("staff")
def staff_profile(request, id):
    # AUTH
    user = request.user
    if request.user.id != id:
        return HttpResponseRedirect(f"/staff/profile/{request.user.id}/")
    return render(request, "dimpro/staff/staff_profile.html")


@only_for("signedin")
def staff_profile_edit(request, id):
    user = request.user
    if request.user.id != id:
        return HttpResponseRedirect(f"/staff/profile/{request.user.id}/")
    if request.method == "POST":
        form = UserEditForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            last_name = form.cleaned_data["last_name"]
            email = form.cleaned_data["email"]
            phonenumber = form.cleaned_data["phonenumber"]

            if email is None or name is None or last_name is None:
                return render(
                    request,
                    "dimpro/staff/staff_profile_edit.html",
                    {"message": "Debe rellenar los campos.", "form": form},
                )

            elif not ("@gmail.com" in email or "@outlook.com" in email):
                return render(
                    request,
                    "dimpro/staff/staff_profile_edit.html",
                    {"message": "Email no valido.", "form": form},
                )
            else:
                try:
                    registered_user = User.objects.get(email=email)
                    if registered_user.id != id:
                        return render(
                            request,
                            "dimpro/staff/staff_profile_edit.html",
                            {"message": "Usuario ya registrado.", "form": form},
                        )
                except User.DoesNotExist:
                    pass
            user_to_edit = User.objects.get(id=id)
            user_to_edit.name = name
            user_to_edit.last_name = last_name
            user_to_edit.email = email
            user_to_edit.phonenumber = phonenumber
            user_to_edit.save()
            messages.success(request, "Perfil editado exitosamente.")
            return HttpResponseRedirect(f"/staff/profile/{id}/")
        else:
            return render(
                request, "dimpro/staff/staff_profile_edit.html", {"form": form}
            )
    user = request.user
    data = {
        "name": request.user.name,
        "last_name": request.user.last_name,
        "email": request.user.email,
        "phonenumber": request.user.phonenumber,
    }
    return render(
        request,
        "dimpro/staff/staff_profile_edit.html",
        {"user": user, "form": UserEditForm(data=data)},
    )


@only_for("signedin")
def staff_changepw(request, id):
    user = request.user
    if request.user.id != id:
        return HttpResponseRedirect(f"/staff/profile/{request.user.id}/")
    if request.method == "POST":
        form = ChangePasswordForm(request.POST)
        if form.is_valid():

            usertocheck = User.objects.get(id=request.user.id)
            opassword = form.cleaned_data["opassword"]
            npassword = form.cleaned_data["npassword"]
            cnpassword = form.cleaned_data["cnpassword"]

            if not usertocheck.check_password(opassword):
                return render(
                    request,
                    "dimpro/staff/staff_register.html",
                    {"message": "Contraseña incorrecta.", "form": form},
                )
            if npassword != cnpassword:
                return render(
                    request,
                    "dimpro/staff/staff_changepw.html",
                    {
                        "message": "Las nuevas contraseñas deben ser iguales.",
                        "form": form,
                    },
                )

            if len(npassword) < 8:
                return render(
                    request,
                    "dimpro/staff/staff_register.html",
                    {
                        "message": "La contraseña debe tener al menos 8 caracteres.",
                        "form": form,
                    },
                )
            if not any(c.isalpha() for c in npassword):
                return render(
                    request,
                    "dimpro/staff/staff_register.html",
                    {
                        "message": "La contraseña debe contener letras del alfabeto.",
                        "form": form,
                    },
                )
            nuser = User.objects.get(email=user.email)

            nuser.set_password(npassword)
            nuser.save()
            newuser = authenticate(request, username=user.email, password=npassword)
            login(request, newuser)
            messages.success(request, "Contraseña actualizada exitosamente.")
            return HttpResponseRedirect(f"/staff/profile/{id}/")
        else:
            return render(request, "dimpro/staff/staff_changepw.html", {"form": form})
    return render(
        request,
        "dimpro/staff/staff_changepw.html",
        {"user": user, "form": ChangePasswordForm()},
    )


@only_for("operator")
def delete_user(request, id):
    user = User.objects.get(id=id)
    user.delete()
    messages.success(request, "Usuario eliminado exitosamente.")
    return HttpResponseRedirect(reverse("dimpro:staff_settings"))


@only_for("operator")
def staff_settings(request):
    return render(request, "dimpro/staff/staff_settings.html")


@only_for("operator")
def list_employees(_request):
    employeequery = User.objects.filter(is_staff=True, is_superuser=False).exclude(
        is_operator=True
    )
    data = {"employees": []}
    for user in employeequery:
        date_joined = (
            user.date_joined.strftime("%d %B %Y %H:%M")
            if user.date_joined
            else "No se ha unido aún"
        )
        last_login = (
            user.last_login.strftime("%d %B %Y %H:%M")
            if user.last_login
            else "No ha iniciado sesión aún"
        )
        order_dict = {
            "id": user.id,
            "username": f"{user.name} {user.last_name}",
            "date_joined": date_joined,
            "last_login": last_login,
            "email": user.email,
            "phonenumber": user.phonenumber,
            "orders": user.user_orders(),
        }
        data["employees"].append(order_dict)
    return JsonResponse(data)


@only_for("operator")
def staff_employees(request):
    return render(request, "dimpro/staff/staff_employees.html")


@only_for("operator")
def staff_register_employee(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            last_name = form.cleaned_data["last_name"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            rpassword = form.cleaned_data["rpassword"]
            phonenumber = form.cleaned_data["phonenumber"]
            if password != rpassword:
                return render(
                    request,
                    "dimpro/staff/staff_register.html",
                    {"message": "Las contraseñas no coinciden.", "form": form},
                )

            if len(password) < 8:
                return render(
                    request,
                    "dimpro/staff/staff_register.html",
                    {
                        "message": "La contraseña debe tener al menos 8 caracteres.",
                        "form": form,
                    },
                )
            if not any(c.isalpha() for c in password):
                return render(
                    request,
                    "dimpro/staff/staff_register.html",
                    {
                        "message": "La contraseña debe contener letras del alfabeto.",
                        "form": form,
                    },
                )
            if email is None or name is None or last_name is None:
                return render(
                    request,
                    "dimpro/staff/staff_register.html",
                    {"message": "Debe rellenar los campos.", "form": form},
                )

            elif not ("@gmail.com" in email or "@outlook.com" in email):
                return render(
                    request,
                    "dimpro/staff/staff_register.html",
                    {"message": "Email no valido.", "form": form},
                )
            else:
                try:
                    User.objects.get(email=email)
                    return render(
                        request,
                        "dimpro/staff/staff_register.html",
                        {"message": "Usuario ya registrado.", "form": form},
                    )

                except User.DoesNotExist:
                    pass

            user = authenticate(request, username=email, password=password)
            if user is None:
                User.objects.create_staff(
                    name=name,
                    last_name=last_name,
                    email=email,
                    password=password,
                    phonenumber=phonenumber,
                )
                messages.success(request, "Usuario registrado exitosamente.")
                return HttpResponseRedirect(reverse("dimpro:staff_employees"))
            else:
                return render(
                    request,
                    "dimpro/staff/staff_register.html",
                    {"message": "Usuario ya registrado.", "form": form},
                )
        else:
            return render(request, "dimpro/staff/staff_register.html", {"form": form})
    return render(
        request, "dimpro/staff/staff_register.html", {"form": UserRegisterForm()}
    )


@only_for("operator")
def staff_changetk(request):
    account = AlegraUser.objects.get(id=1)
    if request.method == "POST":
        form = AlegraUserForm(request.POST)
        if form.is_valid():
            account.email = form.cleaned_data["email"]
            account.token = form.cleaned_data["token"]
            account.save()
            messages.info(request, "Token de Alegra actualizado.")
            return HttpResponseRedirect(reverse("dimpro:staff_settings"))
        else:
            return render(request, "dimpro/staff/staff_changetk.html", {"form": form})
    data = {"email": account.email, "token": account.token}
    return render(
        request, "dimpro/staff/staff_changetk.html", {"form": AlegraUserForm(data=data)}
    )


@only_for("operator")
def staff_updatedb(request):
    update()
    messages.info(request, "La base de datos ha sido actualizada.")
    return HttpResponseRedirect(reverse("dimpro:staff_settings"))


@only_for("staff")
def staff_changestatus(request, id):
    order = Order.objects.get(id=id)
    contact = Contact.objects.get(id=order.client_id.id)
    user = User.objects.get(id=order.user_email.id)
    if order.status == "pendiente":
        """ NOT DEPLOYED BECAUSE OF CPANEL'S ISSUES
        # Assamble email
        pdf = export_orderpdf(request, id)
       
        # Create message
        email_subject = 'Tu orden de DIMPRO está preparada'
        email_body = f'Hola, {user.name}, tu pedido de DIMPRO para {contact.name} está preparado'

        email = EmailMessage (
            subject=email_subject,
            body=email_body,
            from_email=settings.EMAIL_HOST_USER,
            to=[user.email],

        )

        # Attach the pdf
        pdf_filename = f'order_{id}_{contact.name}.pdf'
        email.attach(pdf_filename, pdf.getvalue(), 'application/pdf')

        # Send email
        email.send()
        """

        order.status = "preparado"
        order.save()
    else:
        order.status = "pendiente"
        order.save()
    messages.success(request, "Estatus cambiado exitosamente")
    return HttpResponseRedirect(f"/staff/view/order/{order.id}")


@only_for("user")
def index(request):
    user = request.user
    return render(request, "dimpro/client/client_dashboard.html", {"user": user})


@only_for("user")
def client_profile(request, id):
    # AUTH
    user = request.user
    if request.user.id != id:
        return HttpResponseRedirect(f"/client/profile/{request.user.id}/")
    return render(request, "dimpro/client/client_profile.html")


@only_for("user")
def client_orders(request, id):
    user = request.user

    try:
        list_of_orders = Order.objects.filter(user_email=id).order_by("-date")
        number_of_orders = list_of_orders.count()
    except Order.DoesNotExist:
        list_of_orders = []
        number_of_orders = 0
    except User.DoesNotExist:
        number_of_sellers = 0
    return render(
        request,
        "dimpro/client/client_orders.html",
        {"user": user, "orders": list_of_orders, "n_orders": number_of_orders},
    )


@only_for("user")
def client_orders_add(request, id):
    if id != request.user.id:
        return HttpResponseRedirect(reverse("dimpro:index"))

    if request.method == "POST":
        
            user_id = User.objects.get(id=request.POST.get("user_id"))
            try:
                client_id = Contact.objects.get(name=request.POST.get("client_id"))
            except Contact.DoesNotExist:
                messages.error(request, "El cliente no existe.")
                return HttpResponseRedirect(f"/client/order/add/{user_id.id}/")
            
            status = "pendiente"

            new_order = Order.objects.create(
                user_email=user_id,
                client_id=client_id,
                status="pendiente",
                total=0,
            )
            new_order.save(force_update=True)
            return HttpResponseRedirect(f"/client/order/edit/{new_order.id}/")
        

    user = request.user
    list_of_clients = Contact.objects.all()
    return render(
        request,
        "dimpro/client/client_create_order.html",
        {"clients": list_of_clients, "user": user},
    )


@only_for("user")
def client_orders_edit(request, id):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            for product in Order_Product.objects.filter(order_id=Order.objects.get(id=id)):
                product.delete()
    
            for row in data:
                quantity = int(row["quantity"])
                cost = float(row["cost"])
                order = Order.objects.get(id=id)
                product = Product.objects.filter(item=row["item"]).order_by("id").first()
                price = float(row["price"])
                if quantity <= 0:
                    continue
                else:
                    
                    new_product = Order_Product.objects.create(
                        order_id=order,
                        product_id=product,
                        quantity=quantity,
                        cost=cost,
                        price=price,
                    )
                    new_product.save(force_update=True)


        except Exception:
            total = request.POST.get("total-tosubmit")
            pricetype = request.POST.get("price-tosubmit")
            order = Order.objects.get(id=id)
            type = request.POST.get("order-type").lower()
            order.pricetype = pricetype
            order.total = total
            order.type = type
            order.save()
        messages.success(request, "Pedido actualizado exitosamente.")
        return HttpResponseRedirect(f"/client/order/view/{id}/")

    else:
        order = Order.objects.get(id=id)
        products = Product.objects.filter(price__gt=0)
        pricetypes = PriceType.objects.all()
        try:
            percentage = PriceType.objects.get(name = order.pricetype).percentage
        except PriceType.DoesNotExist:
            percentage = 0
        return render(
            request,
            "dimpro/client/client_edit_order.html",
            {"order": order, "products": products, "pricetypes": pricetypes, "percentage": percentage, "note":Note.objects.get(name = "ADVERTENCIA")},
        )


@only_for("user")
def client_order_view(request, id):
    if request.method == "POST":
        pass
    order = Order.objects.get(id=id)
    client = User.objects.get(email=order.user_email)
    return render(
        request,
        "dimpro/client/client_order_view.html",
        {
            "seller": client,
            "order": order,
            "client": order.client_id.name,
            "order_categories": order.product_categories(),
        },
    )


@only_for("user")
def client_order_delete(request, id):
    order = Order.objects.get(id=id)
    if order.status == "preparado":
        messages.error(request, "No se puede eliminar un pedido preparado.")
        return HttpResponseRedirect(f"/client/orders/{order.user_email.id}/")
    if request.user.id != order.user_email.id:
        return HttpResponseRedirect(reverse("dimpro:index"))

    order.delete()
    messages.success(request, "Pedido eliminado exitosamente.")
    return HttpResponseRedirect(f"/client/orders/{order.user_email.id}/")


@only_for("operator")
def staff_order_delete(request, id):
    order = Order.objects.get(id=id)
    order.delete()
    messages.success(request, "Pedido eliminado exitosamente.")
    return HttpResponseRedirect(f"/client/orders/{order.user_email.id}/")


@only_for("staff")
def list_contacts_all(_request):
    contacts = Contact.objects.all()
    data = {"contacts": []}
    for contact in contacts:
        contact_dict = {
            "name": contact.id,
        }
        data["contacts"].append(contact_dict)
    return JsonResponse(data)


@only_for("operator")
def verify_password(request):
    user = request.user
    if request.method == "POST":
        form = CheckOperatorPasswordForm(request.POST)
        usertocheck = User.objects.get(id=user.id)

        if form.is_valid():
            password = form.cleaned_data["password"]
            if usertocheck.check_password(password):
                return HttpResponseRedirect(reverse("dimpro:staff_changetk"))
            else:
                return render(
                    request,
                    "dimpro/staff/staff_authenticate.html",
                    {
                        "user": request.user,
                        "message": "Contraseña incorrecta.",
                        "form": form,
                    },
                )
        return render(
            request,
            "dimpro/staff/staff_authenticate.html",
            {"user": request.user, "form": form},
        )
    return render(
        request,
        "dimpro/staff/staff_authenticate.html",
        {"user": request.user, "form": CheckOperatorPasswordForm()},
    )


def export_orderpdf(request, id):
    # Create bytestream buffer
    buf = io.BytesIO()
    # Create a BaseDocTemplate
    doc = BaseDocTemplate(buf, pagesize=letter)
    # Create a frame
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id='normal')
    
    # Create a PageTemplate
    template = PageTemplate(id='test', frames=frame)

    # Add PageTemplate to the BaseDocTemplate
    doc.addPageTemplates([template])


    #Add headings
    lines = [["ID", "Item", "Referencia", "Cantidad", "Precio", "Subtotal"]]

    order = Order.objects.get(id=id)
    products = Order_Product.objects.filter(order_id=id)
    
    for product in products:
        product_id = Paragraph(str(product.product_id.id), styles['Normal'])
        item = Paragraph(str(product.product_id.item), styles['Normal'])
        reference = Paragraph(str(product.product_id.reference), styles['Normal'])
        quantity = Paragraph(str(product.quantity), styles['Normal'])
        price = Paragraph(str(product.price) + "$", styles['Normal'])
        cost = Paragraph(str(product.cost) + "$", styles['Normal'])

        lines.append((product_id, 
                     item, 
                     reference, 
                     quantity, 
                     price, 
                     cost))
    
    col_widths = [10*mm, 75*mm, 25*mm, 17*mm, 20*mm, 23*mm]
    
    table = Table(lines, colWidths=col_widths, rowHeights=10*mm)

    table.setStyle(TableStyle([
                        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # Vertically center-align all cells
                        ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                        ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
                        ('FONTSIZE', (0,0), (-1,0), 10),
                        ('FONTSIZE', (0,1), (-1,-1), 7),

    ]))
    
    # Create logo 
    drawing = svg2rlg(finders.find('dimpro/logodimpro.svg'))
    drawing.width = 100
    drawing.height = 0
    drawing.hAlign = 'CENTER'
    seller = User.objects.get(email=order.user_email)

    # Create Paragraph of information
    
    information = Paragraph(f"<b>ID de pedido:</b> {order.id}<br/><b>Tipo de precio:</b> {order.pricetype}<br/><b>Cliente: </b>{Contact.objects.get(id=order.client_id.id).name}<br/><b>Vendedor:</b> {seller.name} {seller.last_name}<br/><b>Email del Vendedor:</b> { seller.email }<br/><b>Items:</b> {len(Order_Product.objects.filter(order_id=id))}<br/><b>Total:</b> {order.total}$<br/><b>Fecha:</b> {order.date.strftime('%d %B %Y %H:%M')}", styles["Normal"])

    # Create a spacer
    spacer = Spacer(1, 12)

    # Create story
    story = [drawing, spacer, information, spacer, table]

    # Add table to BaseDocTemplate
    doc.build(story)
    buf.seek(0)

    
    return FileResponse(buf, as_attachment=True, filename=f'order{order.id}{order.client_id.name}.pdf')

@csrf_exempt
def send_push(request):
    try:
        body = request.body
        data = json.loads(body)

        if 'head' not in data or 'body' not in data or 'id' not in data:
            return JsonResponse(status=400, data={'message':'Invalid data format'})
        
        payload = {'head': data['head'], 'body': data['body']}

        staff_users = User.objects.filter(is_staff=True)  # get all staff users

        for user in staff_users:
            send_user_notification(user=user, payload=payload, ttl=1000)


        return JsonResponse(status=200, data={'message': 'Web push succesful'})
    except TypeError:
        return JsonResponse(status=500, data={'mesage': 'An error occurred'})
    
def change_warning(request):
    try:
        body = request.body
        data = json.loads(body)
        text = data['note']
        try:
            warning = Note.objects.get(name="ADVERTENCIA")
            warning.note = text
            warning.save() 
            return JsonResponse(status=200, data={'message': f'Warning updated with "{text}"'})
        except Note.DoesNotExist:
            return JsonResponse(status=400, data={'message':'Warning object does not exist'})
    except TypeError:
        return JsonResponse(status=500, data={'mesage': 'An error occurred, data is not a JSON'})