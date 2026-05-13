from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from main.models import Employee, Work_Schedule
from main.serializers.admin.schedule.serializers import (
    AdminEmployeeScheduleSerializer,
)


class AdminEmployeeScheduleCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            employee = Employee.objects.get(id=pk)
        except Employee.DoesNotExist:
            return Response({"error": "Співробітника не знайдено"}, status=404)

        serializer = AdminEmployeeScheduleSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(employee=employee)

            return Response(
                {
                    "message": "Розклад успішно додано",
                    "schedule": serializer.data,
                },
                status=201,
            )

        return Response(serializer.errors, status=400)
