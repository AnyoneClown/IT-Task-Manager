from django.contrib.auth.views import LogoutView
from django.urls import path
from authentication.views import register_view, ChangePasswordView

urlpatterns = [
    path("register/", register_view, name="sign-up"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("change-password/", ChangePasswordView.as_view(), name="password_change"),
]

app_name = "authentication"
