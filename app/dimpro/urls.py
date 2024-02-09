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
    path("staff/sellers/", views.staff_clients, name='staff_clients'),
    path("staff/view/seller/<int:id>", views.staff_client_view, name='staff_client_view'),
    path("staff/view/order/<int:id>", views.staff_order_view, name='staff_order_view'),
    path("logout/", views.logout_action, name='logout'),
    path("list_orders/", views.list_orders_start, name='list_orders'),
    path("list_orders/all/", views.list_orders_all, name='list_orders_all'),
    path("list_sellers/", views.list_sellers, name="list-sellers"),
    path("list_orders/user/<int:id>", views.list_orders_user, name='list_orders_user'),
    path("list_products_order/order/<int:id>", views.list_products_for_order, name='list_products_for_order'),
    path("staff/view/order/<int:id>/add", views.add_order_popup, name='add_order_popup')
]