from django.urls import path
from django.contrib.auth.views import LoginView
from . import views

app_name = "users"

urlpatterns = [
    path(
        "login/",
        LoginView.as_view(
            template_name="users/login.html",
            redirect_authenticated_user=True,
        ),
        name="login",
    ),
    path("logout/", views.logout_view, name="logout"),

    path("register/", views.register, name="register"),
    path("profile/", views.profile, name="profile"),
    path("list/", views.users_list, name="users_list"),

    path("groups/", views.groups_list, name="groups_list"),
    path("groups/<int:pk>/join/", views.group_join, name="group_join"),
    path("groups/<int:pk>/leave/", views.group_leave, name="group_leave"),
    path("groups/<int:pk>/", views.group_detail, name="group_detail"),

    path("<str:username>/", views.public_profile, name="public_profile"),
]
