from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse, HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views import generic

from task_manager.models import Task
from task_manager.forms import WorkerUpdateForm, TaskCreateForm


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
    paginate_by = 5
    context_object_name = "task_list"
    template_name = "task_manager/task_list.html"


class MyCompletedTaskListView(LoginRequiredMixin, generic.ListView):
    model = Task
    paginate_by = 5
    context_object_name = "task_list"
    template_name = "task_manager/my_completed_task_list.html"

    def get_queryset(self):
        return Task.objects.filter(assignees=self.request.user, is_completed=True).prefetch_related("assignees")


class MyInProgressTaskListView(LoginRequiredMixin, generic.ListView):
    model = Task
    paginate_by = 5
    context_object_name = "task_list"
    template_name = "task_manager/my_in_progress_task_list.html"

    def get_queryset(self):
        return Task.objects.filter(assignees=self.request.user, is_completed=False).prefetch_related("assignees")


class TaskDetailView(LoginRequiredMixin, generic.DetailView):
    model = Task
    queryset = Task.objects.all().select_related("task_type").prefetch_related("assignees")

    def get_context_data(self, **kwargs):
        context = super(TaskDetailView, self).get_context_data(**kwargs)
        context["assignees"] = ", ".join(assignee.username for assignee in self.object.assignees.all())
        return context


class TaskCreateView(LoginRequiredMixin, generic.CreateView):
    model = Task
    form_class = TaskCreateForm
    success_url = reverse_lazy("task-manager:task-list")


class WorkerListView(LoginRequiredMixin, generic.ListView):
    model = get_user_model()
    paginate_by = 5
    context_object_name = "worker_list"
    template_name = "task_manager/worker_list.html"


class WorkerDetailView(LoginRequiredMixin, generic.DetailView):
    model = get_user_model()


class WorkerUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = get_user_model()
    form_class = WorkerUpdateForm
    success_url = reverse_lazy("task-manager:worker-list")

    def dispatch(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated and user.id != int(kwargs['pk']):
            return render(request, "task_manager/page-403.html")
        return super(WorkerUpdateView, self).dispatch(request, *args, **kwargs)


class WorkerDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = get_user_model()
    success_url = reverse_lazy("authentication:sign-up")

    def dispatch(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated and user.id != int(kwargs['pk']):
            return render(request, "task_manager/page-403.html")
        return super(WorkerDeleteView, self).dispatch(request, *args, **kwargs)


@login_required
def complete_task(request, pk):
    task = get_object_or_404(Task, pk=pk)

    if task.is_completed:
        task.is_completed = False
    else:
        task.is_completed = True
    task.save()
    return redirect(reverse_lazy("task-manager:task-detail", args=[pk]))
