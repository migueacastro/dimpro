from django.urls import path, include
from . import views

app_name = 'dimpro'
urlpatterns = [
    path("", views.index, name="index"),
    path("start/", views.start, name="start"),
    path("login/", views.login_user, name="login_user"),
    path("login_staff/", views.login_staff, name='login_staff'),
    path("register/", views.register, name='register'),
    path("staff/dashboard/", views.control, name='control'),
    path("staff/orders/", views.staff_orders, name='staff_orders'),
    path("staff/clients/", views.staff_clients, name='staff_clients'),
    path("staff/view/client/<int:id>", views.staff_client_view, name='staff_client_view'),
    path("staff/view/order/<int:id>", views.staff_order_view, name='staff_order_view'),
    path("logout/", views.logout_action, name='logout')
]