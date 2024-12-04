from django.urls import path

from tracker.apps import TrackerConfig
from tracker.views import (BusyEmployeesView, EmployeeCreateAPIView,
                           EmployeeDestroyAPIView, EmployeeListAPIView,
                           EmployeeRetrieveAPIView, EmployeeUpdateAPIView,
                           ImportantTasksView, TaskCreateAPIView,
                           TaskDestroyAPIView, TaskListAPIView,
                           TaskRetrieveAPIView, TaskUpdateAPIView)

app_name = TrackerConfig.name

urlpatterns = [
    path("employee_list/", EmployeeListAPIView.as_view(), name="employee-list"),
    path("employee_create/", EmployeeCreateAPIView.as_view(), name="employee-create"),
    path(
        "employee_update/<int:pk>/",
        EmployeeUpdateAPIView.as_view(),
        name="employee-update",
    ),
    path(
        "employee_destroy/<int:pk>/",
        EmployeeDestroyAPIView.as_view(),
        name="employee-destroy",
    ),
    path(
        "employee_retrieve/<int:pk>/",
        EmployeeRetrieveAPIView.as_view(),
        name="employee-retrieve",
    ),
    path("task_list/", TaskListAPIView.as_view(), name="task-list"),
    path("task_create/", TaskCreateAPIView.as_view(), name="task-create"),
    path("task_update/<int:pk>/", TaskUpdateAPIView.as_view(), name="task-update"),
    path("task_destroy/<int:pk>/", TaskDestroyAPIView.as_view(), name="task-destroy"),
    path(
        "task_retrieve/<int:pk>/", TaskRetrieveAPIView.as_view(), name="task-retrieve"
    ),
    path("employees/busy/", BusyEmployeesView.as_view(), name="busy-employees"),
    path("tasks/important/", ImportantTasksView.as_view(), name="important-tasks"),
]
