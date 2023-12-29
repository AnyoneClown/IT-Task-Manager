from django.contrib import admin
from django.urls import path, include
urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("authentication.urls", namespace="authentication")),
    path("accounts/", include("django.contrib.auth.urls")),
    path("", include("task_manager.urls", namespace="task-manager")),
]

