from django.urls import path, include
from . import views

app_name = 'dimpro'
urlpatterns = [ 
    path("", views.index, name="index"),

    # AUTH
    path("start/", views.start, name="start"),
    path("login/", views.login_user, name="login_user"),
    path("login_staff/", views.login_staff, name='login_staff'),
    path("register/", views.register, name='register'),
    
    # STAFF
    path("staff/dashboard/", views.control, name='control'),
    path("staff/orders/", views.staff_orders, name='staff_orders'),
    path("staff/sellers/", views.staff_clients, name='staff_clients'),
    path("staff/view/seller/<int:id>", views.staff_client_view, name='staff_client_view'),
    path("staff/view/order/<int:id>", views.staff_order_view, name='staff_order_view'),
    path("logout/", views.logout_action, name='logout'),
    path("list_orders/", views.list_orders_start, name='list_orders'),
    path("list_orders/all/", views.list_orders_all, name='list_orders_all'),
    path("list_sellers/", views.list_sellers, name="list-sellers"),
    path("list_orders/user/<int:id>/", views.list_orders_user, name='list_orders_user'),
    path("list_products_order/order/<int:id>/", views.list_products_for_order, name='list_products_for_order'),
    path("list_products/", views.list_products, name="list_products"),
    path("staff/view/order/edit/<int:id>", views.edit_order, name='edit_order'),
    path("staff/profile/<int:id>/", views.staff_profile, name='staff_profile'),
    path("staff/profile/edit/<int:id>/", views.staff_profile_edit, name='staff_profile_edit'),
    path("staff/profile/changepassword/<int:id>", views.staff_changepw, name='staff_changepw'),
    path("staff/settings/", views.staff_settings, name='staff_settings'),
    path("staff/delete/<int:id>", views.delete_user, name='staff_delete_user'),
    path("list_employees/", views.list_employees, name='list_employees'),
    path("staff/employees/", views.staff_employees, name='staff_employees'),
    path("staff/register_employee/", views.staff_register_employee, name='staff_register'),
    path("staff/change_token/", views.staff_changetk, name='staff_changetk'),
    path("staff/updatedb/", views.staff_updatedb, name='update_db'),
    path("staff/changestatus/<int:id>/", views.staff_changestatus, name='change_status'),
    path("staff/order/delete/<int:id>/", views.staff_order_delete, name='delete_order'),
    
    # CLIENT
    path("", views.index, name='index'),
    path("client/profile/<int:id>/", views.client_profile, name='client_profile'),
    path("client/orders/<int:id>/", views.client_orders, name='client_orders'),
    path("client/order/add/<int:id>/", views.client_orders_add, name='client_addorder'),
    path("client/order/edit/<int:id>/", views.client_orders_edit, name='client_editorder'),
    path("client/order/view/<int:id>", views.client_order_view, name='client_vieworder'),
    path("client/order/delete/<int:id>",  views.client_order_delete, name='client_deleteorder'),
]