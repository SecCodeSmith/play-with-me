from django.urls import path
from api import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login, name="login"),
    path("register/", views.register, name="register"),
    path("tokenCNF/", views.get_csrf_token, name="get_csrf_token"),
    path("sessionStatus/", views.is_auth_session, name="is_auth_session"),
    path("logout/", views.log_out, name="logout"),
    path("langList/", views.get_lang_list, name="get_lang_list"),
    path("lang/", views.get_lang, name="get_lang"),
    path("setDescription/", views.user_set_description, name="user_set_description"),
    path("updatePassword/", views.change_password, name="change_password"),
    path("newFriendship/", views.add_friendship, name="add_friendship"),
    path("invideList/", views.active_friendship_invite, name="active_friendship_invite"),
    path("acceptFriendship/", views.accept_invite, name="accept_invite"),
    path("myProfile/", views.get_my_profile, name="get_my_profile"),
    path("getUser/", views.get_users, name="get_users"),
]
