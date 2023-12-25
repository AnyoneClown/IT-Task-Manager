from django.urls import path

from .views import index, TaskListView, WorkerListView, TaskDetailView, WorkerDetailView

urlpatterns = [
    path("", index, name="index"),
    path("tasks/", TaskListView.as_view(), name="task-list"),
    path("task/<int:pk>/", TaskDetailView.as_view(), name="task-detail"),
    path("workers/", WorkerListView.as_view(), name="worker-list"),
    path("worker/<int:pk>/", WorkerDetailView.as_view(), name="worker-detail"),
]

app_name = "task-manager"
