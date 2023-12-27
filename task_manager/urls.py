from django.urls import path

from .views import index, TaskListView, WorkerListView, TaskDetailView, WorkerDetailView, WorkerUpdateView, WorkerDeleteView, TaskCreateView, MyCompletedTaskListView, MyInProgressTaskListView, complete_task

urlpatterns = [
    path("", index, name="index"),
    path("tasks/", TaskListView.as_view(), name="task-list"),
    path("my_completed_tasks/", MyCompletedTaskListView.as_view(), name="my-completed-task-list"),
    path("my_in_progress_tasks/", MyInProgressTaskListView.as_view(), name="my-in-progress-task-list"),
    path("task/create/", TaskCreateView.as_view(), name="task-create"),
    path("task/<int:pk>/", TaskDetailView.as_view(), name="task-detail"),
    path("task/<int:pk>/complete", complete_task, name="toggle-task-complete"),
    path("workers/", WorkerListView.as_view(), name="worker-list"),
    path("worker/<int:pk>/", WorkerDetailView.as_view(), name="worker-detail"),
    path("worker/<int:pk>/update/", WorkerUpdateView.as_view(), name="worker-update"),
    path("worker/<int:pk>/delete/", WorkerDeleteView.as_view(), name="worker-delete"),
]

app_name = "task-manager"
