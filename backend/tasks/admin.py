from django.contrib import admin
from tasks.models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("title", "status", "priority", "user", "created_at")
    list_filter = ("status", "priority", "user")
    search_fields = ("title", "description", "user__username")
    ordering = ("-created_at",)
    list_editable = ("status", "priority")
    date_hierarchy = "created_at"
    readonly_fields = ("created_at", "updated_at")
