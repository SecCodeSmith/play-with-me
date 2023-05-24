from django.urls import path
import rest_framework

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login, name="login"),
    path("register", views.register, name="register"),
    path("tokenCNF", views.get_csrf_token, name="token"),
]