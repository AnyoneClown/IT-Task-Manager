from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


class Worker(AbstractUser):
    position = models.ForeignKey("Position", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "worker"
        verbose_name_plural = "workers"

    def __str__(self) -> str:
        return f"Username: {self.username} FL: {self.first_name} {self.last_name}"

    def get_absolute_url(self):
        return reverse("task-manager:worker-detail", kwargs={"pk": self.pk})


class Position(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name


class TaskType(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name


class Task(models.Model):
    PRIORITY_CHOICES = (
        ("UR", "Urgent"),
        ("HG", "High"),
        ("MD", "Medium"),
        ("LW", "Low"),
    )

    name = models.CharField(max_length=255)
    description = models.TextField()
    deadline = models.DateTimeField()
    is_completed = models.BooleanField()
    priority = models.CharField(max_length=2, choices=PRIORITY_CHOICES, default="LW")
    task_type = models.ForeignKey(TaskType, on_delete=models.CASCADE)
    assignees = models.ManyToManyField(get_user_model(), related_name="tasks")

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self):
        return reverse("task-manager:task-detail", kwargs={"pk": self.pk})

    def get_priority_display(self) -> str:
        return dict(self.PRIORITY_CHOICES).get(self.priority, self.priority)
