from django import forms
from django.contrib.auth import get_user_model
from django.forms import CheckboxSelectMultiple, SplitDateTimeWidget

from task_manager.models import Position, Task, TaskType


class WorkerUpdateForm(forms.ModelForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Username",
                "class": "form-control"
            }
        )
    )
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "placeholder": "Email",
                "class": "form-control"
            }
        )
    )
    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "First name",
                "class": "form-control"
            }
        )
    )
    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Last name",
                "class": "form-control"
            }
        )
    )
    position = forms.ModelChoiceField(
        queryset=Position.objects.all(),
        widget=forms.Select(
            attrs={
                "placeholder": "Last name",
                "class": "form-control"
            }
        )
    )

    class Meta:
        model = get_user_model()
        fields = ("username", "email", "first_name", "last_name", "position")


class TaskCreateForm(forms.ModelForm):
    PRIORITY_CHOICES = (
        ("UR", "Urgent"),
        ("HG", "High"),
        ("MD", "Medium"),
        ("LW", "Low"),
    )

    name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Name",
                "class": "form-control"
            }
        )
    )
    description = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "placeholder": "Description",
                "class": "form-control"
            }
        )
    )
    deadline = forms.DateTimeField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'type': 'text',
                'placeholder': 'Deadline',
                'id': 'id_deadline',
            }
        ),
        input_formats=['%Y-%m-%d %H:%M:%S'],
    )

    priority = forms.ChoiceField(
        choices=PRIORITY_CHOICES,
        widget=forms.Select(
            attrs={
                "placeholder": "Priority",
                "class": "form-control"
            }
        )
    )
    task_type = forms.ModelChoiceField(
        queryset=TaskType.objects.all(),
        widget=forms.Select(
            attrs={
                "placeholder": "Task Type",
                "class": "form-control"
            }
        )
    )
    assignees = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.SelectMultiple(
            attrs={
                "placeholder": "Assignees",
                "class": "form-control"
            }
        )
    )

    class Meta:
        model = Task
        fields = ["name", "description", "deadline", "priority", "task_type", "assignees"]

    def save(self, commit=True):
        task = super(TaskCreateForm, self).save(commit=False)
        task.is_completed = False
        if commit:
            task.save()
            self.save_m2m()
        return task