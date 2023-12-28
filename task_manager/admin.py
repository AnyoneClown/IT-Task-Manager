from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from task_manager.models import Worker, Task, Position, TaskType


@admin.register(Worker)
class WorkerAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ("position",)
    fieldsets = UserAdmin.fieldsets + (
        (("Additional info", {"fields": ("position",)}),)
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            (
                "Additional info",
                {
                    "fields": (
                        "first_name",
                        "last_name",
                        "position",
                    )
                },
            ),
        )
    )


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "deadline",
        "is_completed",
        "priority",
        "task_type",
        "display_assignees",
    )
    search_fields = ("name",)
    list_filter = ("priority", "is_completed")

    def display_assignees(self, obj):
        return ", ".join([assignee.username for assignee in obj.assignees.all()])

    display_assignees.short_description = "Assignees"


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    search_fields = ("name",)
    list_filter = ("name",)


@admin.register(TaskType)
class TaskTypeAdmin(admin.ModelAdmin):
    search_fields = ("name",)
    list_filter = ("name",)
