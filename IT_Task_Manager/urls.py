from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path("accounts/", include("authentication.urls", namespace="authentication")),
    path("", include("task_manager.urls", namespace="task-manager")),
]
