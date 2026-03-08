from rest_framework import serializers
from main.models import (
    Service_Guide,
    Employee,
    Position_Service,
    Work_Schedule,
    Position,
)


class WorkScheduleSerializers(serializers.ModelSerializer):
    class Meta:
        model = Work_Schedule
        fields = ["day_of_week", "start_time", "end_time"]


class PositionSerializers(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = ["name"]


class EmployeeSerializers(serializers.ModelSerializer):
    position = PositionSerializers(read_only=True)
    schedule = WorkScheduleSerializers(
        many=True, read_only=True, source="work_schedule_set"
    )

    class Meta:
        model = Employee
        fields = ["first_name", "last_name", "middle_name", "position", "schedule"]


class ServiceGuideSerializer(serializers.ModelSerializer):
    price = serializers.SerializerMethodField()

    class Meta:
        model = Service_Guide
        fields = ["id", "name", "description", "price"]

    def get_price(self, obj):
        return int(obj.price)


class PositionServiceSerializers(serializers.ModelSerializer):
    service = ServiceGuideSerializer(read_only=True)
    employees = serializers.SerializerMethodField()

    class Meta:
        model = Position_Service
        fields = ["service", "employees"]

    def get_employees(self, obj):
        employees = Employee.objects.filter(position=obj.position).prefetch_related(
            "work_schedule_set"
        )
        return EmployeeSerializers(employees, many=True).data
