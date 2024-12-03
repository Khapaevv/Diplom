from django.contrib import admin
from .models import Employee, Task

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ("id", "full_name", "position", "created_at")
    search_fields = ("full_name", "position")

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "employee", "deadline", "status", "created_at")
    list_filter = ("status", "deadline")
    search_fields = ("name",)