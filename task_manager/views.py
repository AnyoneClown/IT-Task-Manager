from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views import generic

from task_manager.models import Task


@login_required
def index(request: HttpRequest) -> HttpResponse:
    num_workers = get_user_model().objects.count()
    completed_tasks = Task.objects.filter(is_completed=True).count()
    num_tasks = Task.objects.count()

    context = {
        "num_workers": num_workers,
        "completed_tasks": completed_tasks,
        "num_tasks": num_tasks,
    }
    return render(request, "task_manager/index.html", context=context)


class TaskListView(LoginRequiredMixin, generic.ListView):
    model = Task
    context_object_name = "task_list"
    template_name = "task_manager/task_list.html"


class TaskDetailView(LoginRequiredMixin, generic.DetailView):
    model = Task
    queryset = Task.objects.all().select_related("task_type").prefetch_related("assignees")

    def get_context_data(self, **kwargs):
        context = super(TaskDetailView, self).get_context_data(**kwargs)
        context["assignees"] = ", ".join(assignee.username for assignee in self.object.assignees.all())
        return context


class WorkerListView(LoginRequiredMixin, generic.ListView):
    model = get_user_model()
    context_object_name = "worker_list"
    template_name = "task_manager/worker_list.html"


class WorkerDetailView(LoginRequiredMixin, generic.DetailView):
    model = get_user_model()
