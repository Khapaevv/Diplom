from django.db.models import Count, Q
from rest_framework import status
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
)
from rest_framework.response import Response
from rest_framework.views import APIView

from tracker.models import Employee, Task
from tracker.serializers import EmployeeSerializer, TaskSerializer


class EmployeeListAPIView(ListAPIView):
    """Класс для вывода всех сотрудников."""

    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer


class EmployeeRetrieveAPIView(RetrieveAPIView):
    """Класс для просмотра детальной информации о сотруднике."""

    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer


class EmployeeCreateAPIView(CreateAPIView):
    """Класс для создания сотрудника."""

    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer


class EmployeeUpdateAPIView(UpdateAPIView):
    """Класс для редактирования сотрудников."""

    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer


class EmployeeDestroyAPIView(DestroyAPIView):
    """Класс для удаления сотрудников."""

    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer


class TaskListAPIView(ListAPIView):
    """Класс для вывода всех задач."""

    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class TaskRetrieveAPIView(RetrieveAPIView):
    """Класс для просмотра детальной информации о задаче."""

    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class TaskCreateAPIView(CreateAPIView):
    """Класс для создания задачи."""

    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class TaskUpdateAPIView(UpdateAPIView):
    """Класс для редактирования задачи."""

    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class TaskDestroyAPIView(DestroyAPIView):
    """Класс для удаления задачи."""

    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class BusyEmployeesView(APIView):
    """Эндпоинт для получения занятых сотрудников."""

    def get(self, request):
        # Подсчет задач "в работе" для каждого сотрудника
        employees = (
            Employee.objects.annotate(
                active_tasks_count=Count("tasks", filter=Q(tasks__status="in_progress"))
            )
            .filter(
                active_tasks_count__gt=0
            )  # Учитываем только тех, у кого есть активные задачи
            .order_by("-active_tasks_count")  # Сортируем по количеству активных задач
        )

        serializer = EmployeeSerializer(employees, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ImportantTasksView(APIView):
    """Эндпоинт для получения списка важных задач."""

    def get(self, request):
        # Задачи, не начатые или завершенные, от которых зависят активные подзадачи
        important_tasks = Task.objects.filter(
            status__in=["not_started", "completed"], subtasks__status="in_progress"
        ).distinct()

        result = []
        for task in important_tasks:
            # Наименее загруженные сотрудники
            min_load = Employee.objects.annotate(task_count=Count("tasks")).aggregate(
                min_count=Count("tasks")
            )["min_count"]
            least_loaded_employees = Employee.objects.annotate(
                task_count=Count("tasks")
            ).filter(task_count=min_load)

            # Сотрудник, выполняющий родительскую задачу
            parent_employee = task.parent_task.employee if task.parent_task else None
            if parent_employee and parent_employee not in least_loaded_employees:
                if parent_employee.tasks.count() <= min_load + 2:
                    least_loaded_employees = list(least_loaded_employees) + [
                        parent_employee
                    ]

            # Формирование данных для текущей задачи
            serialized_task = {
                "task": TaskSerializer(task).data,
                "deadline": task.deadline,
                "employees": EmployeeSerializer(least_loaded_employees, many=True).data,
            }
            result.append(serialized_task)

        return Response(result, status=status.HTTP_200_OK)
