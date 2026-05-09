from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from main.models import Employee
from main.serializers.admin.employee_detail.serializers import (
    AdminEmployeeDetailSerializer,
)
from main.serializers.admin.employee_update.serializers import (
    AdminEmployeeUpdateSerializer,
)


class AdminEmployeeUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            employee = Employee.objects.select_related(
                "user",
                "position",
            ).get(id=pk)
        except Employee.DoesNotExist:
            return Response({"error": "Співробітника не знайдено"}, status=404)

        serializer = AdminEmployeeDetailSerializer(
            employee,
            context={"request": request},
        )
        return Response(serializer.data)

    def patch(self, request, pk):
        try:
            employee = Employee.objects.select_related(
                "user",
                "position",
            ).get(id=pk)
        except Employee.DoesNotExist:
            return Response({"error": "Співробітника не знайдено"}, status=404)

        serializer = AdminEmployeeUpdateSerializer(
            employee,
            data=request.data,
            partial=True,
        )

        if serializer.is_valid():
            serializer.save()

            detail_serializer = AdminEmployeeDetailSerializer(
                employee,
                context={"request": request},
            )
            return Response(
                {
                    "message": "Дані співробітника успішно оновлено",
                    "employee": detail_serializer.data,
                },
                status=200,
            )

        return Response(serializer.errors, status=400)
