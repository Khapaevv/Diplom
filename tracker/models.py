from django.db import models
from django.utils.translation import gettext_lazy as _

NULLABLE = {"blank": True, "null": True}


class Employee(models.Model):
    """Модель сотрудника."""

    full_name = models.CharField(max_length=150, verbose_name="ФИО")
    position = models.CharField(max_length=100, verbose_name="Должность")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Сотрудник"
        verbose_name_plural = "Сотрудники"
        ordering = ["full_name"]

    def __str__(self):
        return self.full_name


class Task(models.Model):
    """Модель задачи."""

    class TaskStatus(models.TextChoices):
        NOT_STARTED = "not_started", _("Не начата")
        IN_PROGRESS = "in_progress", _("В работе")
        COMPLETED = "completed", _("Завершена")

    name = models.CharField(max_length=255, verbose_name="Название задачи")
    parent_task = models.ForeignKey(
        "self",
        **NULLABLE,
        on_delete=models.SET_NULL,
        related_name="subtasks",
        verbose_name="Родительская задача"
    )
    employee = models.ForeignKey(
        Employee,
        **NULLABLE,
        on_delete=models.SET_NULL,
        related_name="tasks",
        verbose_name="Исполнитель"
    )
    deadline = models.DateField(verbose_name="Срок выполнения")
    status = models.CharField(
        max_length=20,
        choices=TaskStatus.choices,
        default=TaskStatus.NOT_STARTED,
        verbose_name="Статус",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Задача"
        verbose_name_plural = "Задачи"
        ordering = ["deadline"]

    def __str__(self):
        return self.name
