from django.urls import path

from .views import index, TaskListView, WorkerListView

urlpatterns = [
    path("", index, name="index"),
    path("tasks/", TaskListView.as_view(), name="task-view"),
    path("workers/", WorkerListView.as_view(), name="worker-view"),
]

app_name = "task-manager"
