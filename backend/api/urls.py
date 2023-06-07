from django.urls import path
from api import views

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("register/", views.RegisterView.as_view(), name="register"),
    path("sessionStatus/", views.IsAuthSessionView.as_view(), name="is_auth_session"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path("langList/", views.GetLangListView.as_view(), name="get_lang_list"),
    path("lang/", views.GetLangView.as_view(), name="get_lang"),
    path("setDescription/", views.UserSetDescriptionView.as_view(), name="user_set_description"),
    path("updatePassword/", views.ChangePasswordView.as_view(), name="change_password"),
    path("newFriendship/", views.AddFriendshipView.as_view(), name="add_friendship"),
    path("invideList/", views.ActiveFriendshipInviteView.as_view(), name="active_friendship_invite"),
    path("acceptFriendship/", views.AcceptInviteView.as_view(), name="accept_invite"),
    path("myProfile/", views.GetMyProgile.as_view(), name="get_my_profile"),
    path("getUser/", views.get_users, name="get_users"),
    path("newEvent/", views.add_new_event, name="add_new_event"),
    path("addEventParticipant/", views.add_participant_to_event, name="add_participant_to_event"),
]
