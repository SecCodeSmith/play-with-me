from django.urls import path
import rest_framework

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login, name="login"),
    path("register", views.register, name="register"),
    path("tokenCNF", views.get_csrf_token, name="token"),
    path("sessionStatus", views.is_auth_session, name="session_status"),
    path("logout", views.log_out, name="logout"),
    path("langList", views.get_lang_list, name="langList"),
]