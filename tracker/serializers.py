import datetime

from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from tracker.models import Employee, Task


class EmployeeSerializer(ModelSerializer):
    """Сериализатор для сотрудников."""
    class Meta:
        model = Employee
        fields = '__all__'

        def validate_full_name(self, value):
            if len(value) < 3:
                raise serializers.ValidationError("Имя должно содержать минимум 3 символа.")
            return value


class TaskSerializer(ModelSerializer):
    # employee = serializers.SlugRelatedField(slug_field='full_name', read_only=True)

    class Meta:
        model = Task
        fields = '__all__'


        def validate_deadline(self, value):
            if value < datetime.date.today():
                raise serializers.ValidationError("Срок выполнения не может быть в прошлом.")
            return value