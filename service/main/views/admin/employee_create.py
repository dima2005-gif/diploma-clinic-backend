from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from main.serializers.admin.employee_create.serializers import (
    AdminEmployeeCreateSerializer,
)


class AdminEmployeeCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = AdminEmployeeCreateSerializer(data=request.data)

        if serializer.is_valid():
            employee = serializer.save()

            return Response(
                {
                    "message": "Співробітника створено. Дані для входу надіслано на електронну пошту.",
                    "id": employee.id,
                    "login": employee.user.username,
                },
                status=201,
            )

        return Response(serializer.errors, status=400)
