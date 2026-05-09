from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from main.models import Service_Guide
from main.serializers.admin.service.serializers import (
    AdminServiceDetailSerializer,
)


class AdminServiceDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            service = Service_Guide.objects.get(id=pk)
        except Service_Guide.DoesNotExist:
            return Response(
                {"error": "Послугу не знайдено"},
                status=404,
            )

        serializer = AdminServiceDetailSerializer(service)

        return Response(serializer.data)
