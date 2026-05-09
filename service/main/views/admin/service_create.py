from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from main.serializers.admin.service_create.serializers import (
    AdminServiceCreateSerializer,
)


class AdminServiceCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = AdminServiceCreateSerializer(data=request.data)

        if serializer.is_valid():
            service = serializer.save()

            return Response(
                {
                    "message": "Послугу успішно створено",
                    "id": service.id,
                },
                status=201,
            )

        return Response(serializer.errors, status=400)
