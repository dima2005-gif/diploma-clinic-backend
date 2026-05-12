from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from main.models import Employee
from main.serializers.admin.employee_detail.serializers import (
    AdminEmployeeDetailSerializer,
)


class AdminEmployeeDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            employee = Employee.objects.select_related("user", "position").get(id=pk)
        except Employee.DoesNotExist:
            return Response({"error": "Співробітника не знайдено"}, status=404)

        serializer = AdminEmployeeDetailSerializer(employee)

        data = serializer.data
        data["is_current_user"] = employee.user == request.user

        return Response(data)
