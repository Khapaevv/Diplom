from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from tracker.models import Employee, Task
from tracker.serializers import EmployeeSerializer


class EmployeeAPITests(APITestCase):
    fixtures = ["fixtures.json"]

    def setUp(self):
        self.list_url = reverse("tracker:employee-list")
        self.create_url = reverse("tracker:employee-create")
        self.update_url = None
        self.retrieve_url = None
        self.destroy_url = None

    def test_get_all_employees(self):
        """
        Тестирует получение списка всех сотрудников
        """
        response = self.client.get(self.list_url)
        employees = Employee.objects.all()
        serializer = EmployeeSerializer(employees, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_new_employee(self):
        """
        Тестирует создание нового сотрудника
        """
        new_employee = {"full_name": "Новый Сотрудник", "position": "Разработчик"}
        response = self.client.post(self.create_url, new_employee)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(
            Employee.objects.filter(full_name=new_employee["full_name"]).exists()
        )

    def test_retrieve_specific_employee(self):
        """
        Тестирует получение конкретного сотрудника по ID
        """
        employee = Employee.objects.first()
        self.retrieve_url = reverse("tracker:employee-retrieve", args=[employee.id])
        response = self.client.get(self.retrieve_url)
        serializer = EmployeeSerializer(employee)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_existing_employee(self):
        """
        Тестирует обновление существующего сотрудника
        """
        employee = Employee.objects.first()
        self.update_url = reverse("tracker:employee-update", args=[employee.id])
        updated_data = {"full_name": "Обновленный Сотрудник", "position": "Тестировщик"}
        response = self.client.put(self.update_url, updated_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        employee.refresh_from_db()
        self.assertEqual(employee.full_name, updated_data["full_name"])
        self.assertEqual(employee.position, updated_data["position"])

    def test_delete_employee(self):
        """
        Тестирует удаление сотрудника
        """
        employee = Employee.objects.first()
        self.destroy_url = reverse("tracker:employee-destroy", args=[employee.id])
        response = self.client.delete(self.destroy_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Employee.objects.filter(id=employee.id).exists())

    def test_retrieve_nonexistent_employee(self):
        nonexistent_id = 9999

        self.retrieve_url = reverse("tracker:employee-retrieve", args=[nonexistent_id])
        response = self.client.get(self.retrieve_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class TaskAPITestCase(APITestCase):
    fixtures = ["fixtures.json"]

    def test_task_list(self):
        response = self.client.get(reverse("tracker:task-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_task_create(self):
        data = {
            "name": "New Task",
            "employee": 1,
            "deadline": "2024-12-31",
            "status": "not_started",
        }
        response = self.client.post(reverse("tracker:task-create"), data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 4)

    def test_task_update(self):
        task = Task.objects.first()
        data = {"name": "Updated Task"}
        response = self.client.patch(
            reverse("tracker:task-update", kwargs={"pk": task.pk}), data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        task.refresh_from_db()
        self.assertEqual(task.name, "Updated Task")

    def test_task_destroy(self):
        task = Task.objects.first()
        response = self.client.delete(
            reverse("tracker:task-destroy", kwargs={"pk": task.pk})
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Task.objects.count(), 2)

    def test_busy_employees(self):
        response = self.client.get(reverse("tracker:busy-employees"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["full_name"], "Иван Иванов")


class ImportantTasksTestCase(APITestCase):
    def setUp(self):
        # Создаем сотрудников
        self.employee = Employee.objects.create(
            full_name="John Doe", position="Developer"
        )
        self.other_employee = Employee.objects.create(
            full_name="Jane Smith", position="Manager"
        )

        # Создаем задачи и подзадачи
        self.parent_task = Task.objects.create(
            name="Parent Task",
            employee=self.employee,
            deadline="2024-12-01",
            status="completed",
        )
        self.subtask = Task.objects.create(
            name="Subtask",
            employee=self.employee,
            deadline="2024-12-02",
            status="in_progress",
            parent_task=self.parent_task,
        )
        # Создаем задачи без подзадач
        self.independent_task = Task.objects.create(
            name="Independent Task",
            employee=self.other_employee,
            deadline="2024-12-01",
            status="not_started",
        )

        self.url_important_tasks = reverse("tracker:important-tasks")

    def test_important_tasks(self):
        # Отправляем GET запрос для получения важных задач
        response = self.client.get(self.url_important_tasks)

        # Проверяем, что ответ успешен
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Проверяем, что задачи присутствуют в ответе
        self.assertGreater(len(response.data), 0)

        # Проверка на наличие родительской задачи
        task_data = response.data[0]
        self.assertEqual(task_data["task"]["name"], "Parent Task")

        # Проверяем, что подзадачи правильно включены в данные задачи
        self.assertIn(
            "employees", task_data
        )  # Должны быть сотрудники, работающие над задачей
