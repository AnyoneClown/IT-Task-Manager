from django.urls import path

from .views import (
    index,
    TaskListView,
    WorkerListView,
    TaskDetailView,
    WorkerDetailView,
    WorkerUpdateView,
    WorkerDeleteView,
    TaskCreateView,
    MyCompletedTaskListView,
    MyInProgressTaskListView,
    complete_task,
    TaskTypeListView,
    TaskTypeUpdateView,
    TaskTypeCreateView,
    TaskTypeDeleteView,
    PositionListView,
    PositionDeleteView,
    PositionUpdateView,
    PositionCreateView,
    TaskDeleteView,
    TaskUpdateView,
    rick_roll,
)
urlpatterns = [
    path("", index, name="index"),
    path("rick_roll/", rick_roll, name="rick-roll"),
    path("tasks/", TaskListView.as_view(), name="task-list"),
    path(
        "my_completed_tasks/",
        MyCompletedTaskListView.as_view(),
        name="my-completed-task-list",
    ),
    path(
        "my_in_progress_tasks/",
        MyInProgressTaskListView.as_view(),
        name="my-in-progress-task-list",
    ),
    path("task/create/", TaskCreateView.as_view(), name="task-create"),
    path("task/<int:pk>/", TaskDetailView.as_view(), name="task-detail"),
    path("task/<int:pk>/update/", TaskUpdateView.as_view(), name="task-update"),
    path("task/<int:pk>/delete/", TaskDeleteView.as_view(), name="task-delete"),
    path("task/<int:pk>/complete", complete_task, name="toggle-task-complete"),
    path("workers/", WorkerListView.as_view(), name="worker-list"),
    path("worker/<int:pk>/", WorkerDetailView.as_view(), name="worker-detail"),
    path("worker/<int:pk>/update/", WorkerUpdateView.as_view(), name="worker-update"),
    path("worker/<int:pk>/delete/", WorkerDeleteView.as_view(), name="worker-delete"),
    path("task_types/", TaskTypeListView.as_view(), name="task-type-list"),
    path("task_type/create/", TaskTypeCreateView.as_view(), name="task-type-create"),
    path(
        "task_types/<int:pk>/update/",
        TaskTypeUpdateView.as_view(),
        name="task-type-update",
    ),
    path(
        "task_types/<int:pk>/delete/",
        TaskTypeDeleteView.as_view(),
        name="task-type-delete",
    ),
    path("position/", PositionListView.as_view(), name="position-list"),
    path("position/create/", PositionCreateView.as_view(), name="position-create"),
    path(
        "position/<int:pk>/update/",
        PositionUpdateView.as_view(),
        name="position-update",
    ),
    path(
        "position/<int:pk>/delete/",
        PositionDeleteView.as_view(),
        name="position-delete",
    ),
]


app_name = "task-manager"
