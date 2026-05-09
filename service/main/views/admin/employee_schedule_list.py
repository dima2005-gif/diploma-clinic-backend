from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from main.models import Employee, Work_Schedule
from main.serializers.admin.employee_schedule.serializers import (
    AdminEmployeeScheduleSerializer,
)


class AdminEmployeeScheduleView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            employee = Employee.objects.get(id=pk)
        except Employee.DoesNotExist:
            return Response({"error": "Співробітника не знайдено"}, status=404)

        schedule = Work_Schedule.objects.filter(employee=employee).order_by("id")

        serializer = AdminEmployeeScheduleSerializer(schedule, many=True)

        return Response(serializer.data)
