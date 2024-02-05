from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("start/", views.start, name="start"),
    path("login/", views.login_user, name="login_user"),
    path("login_staff/", views.login_staff, name='login_staff'),
    path("register/", views.register, name='register'),
]