from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse, HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views import generic

from task_manager.models import Task, TaskType, Position, Worker
from task_manager.forms import WorkerUpdateForm, TaskCreateForm, TaskTypeUpdateForm, TaskTypeCreateForm, \
    PositionUpdateForm, PositionCreateForm, BaseSearchForm, WorkerSearchForm


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


class BaseSearchListView(generic.ListView):
    """
    A base class for Django list views with integrated search functionality.

    Subclasses can inherit from this base class to easily add search capabilities
    to list views. It provides pagination, context object name, and search form handling.

    Attributes:
        paginate_by (int): Number of items per page for pagination.
        context_object_name (str): Name of the variable to use in the template for the list of objects.
        search_form_class (Form): Form class responsible for handling search queries.
        queryset (QuerySet): The base queryset for the list view.
        search_field (str): The field to use for searching.
    """
    paginate_by = 5
    context_object_name = "object_list"
    search_form_class = None
    queryset = None
    search_field = "name"

    def get_queryset(self):
        form = self.search_form_class(self.request.GET)

        if form.is_valid():
            self.queryset = self.queryset.filter(
                **{f"{self.search_field}__icontains": form.cleaned_data["search_query"]}
            )
        return self.queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_form"] = self.search_form_class(
            initial={"search_query": self.request.GET.get("search_query", "")}
        )
        return context


class TaskListView(LoginRequiredMixin, BaseSearchListView):
    model = Task
    template_name = "task_manager/task_list.html"
    queryset = Task.objects.select_related("task_type").prefetch_related("assignees")
    search_form_class = BaseSearchForm
    search_field = "name"


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


class WorkerListView(LoginRequiredMixin, BaseSearchListView):
    model = Worker
    template_name = "task_manager/worker_list.html"
    queryset = Worker.objects.all()
    search_form_class = WorkerSearchForm
    search_field = "username"


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


class TaskTypeListView(LoginRequiredMixin, BaseSearchListView):
    model = TaskType
    template_name = "task_manager/tasktype_list.html"
    queryset = TaskType.objects.filter()
    search_form_class = BaseSearchForm


class TaskTypeCreateView(LoginRequiredMixin, generic.CreateView):
    model = TaskType
    form_class = TaskTypeCreateForm
    success_url = reverse_lazy("task-manager:task-type-list")


class TaskTypeDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = TaskType
    success_url = reverse_lazy("task-manager:task-type-list")


class TaskTypeUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = TaskType
    form_class = TaskTypeUpdateForm
    template_name = "task_manager/tasktype_update_form.html"
    success_url = reverse_lazy("task-manager:task-type-list")


class PositionListView(LoginRequiredMixin, BaseSearchListView):
    model = Position
    template_name = "task_manager/position/position_list.html"
    queryset = Position.objects.all()
    search_form_class = BaseSearchForm


class PositionCreateView(LoginRequiredMixin, generic.CreateView):
    model = Position
    form_class = PositionCreateForm
    template_name = "task_manager/position/position_form.html"
    success_url = reverse_lazy("task-manager:position-list")


class PositionDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Position
    template_name = "task_manager/position/position_confirm_delete.html"
    success_url = reverse_lazy("task-manager:position-list")


class PositionUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Position
    form_class = PositionUpdateForm
    template_name = "task_manager/position/position_update_form.html"
    success_url = reverse_lazy("task-manager:position-list")


@login_required
def complete_task(request, pk):
    task = get_object_or_404(Task, pk=pk)

    if task.is_completed:
        task.is_completed = False
    else:
        task.is_completed = True
    task.save()
    return redirect(reverse_lazy("task-manager:task-detail", args=[pk]))
