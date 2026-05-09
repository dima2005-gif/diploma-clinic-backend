from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from main.models import Employee
from main.serializers.admin.employee_list.serializers import (
    AdminEmployeeListSerializer,
)


class AdminEmployeeListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        employees = (
            Employee.objects.select_related(
                "user",
                "position",
            )
            .all()
            .order_by("id")
        )

        serializer = AdminEmployeeListSerializer(employees, many=True)

        return Response(serializer.data)
