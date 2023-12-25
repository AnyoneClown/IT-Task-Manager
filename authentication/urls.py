from django.contrib.auth.views import LogoutView
from django.urls import path
from authentication.views import register_view

urlpatterns = [
    path("register/", register_view, name="sign-up"),
    path("logout/", LogoutView.as_view(), name="logout")
]

app_name = "authentication"
