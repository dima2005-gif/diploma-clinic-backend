from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from main.models import Service_Guide
from main.serializers.guest.service_detail.serializers import (
    GuestServiceDetailSerializer,
)


class GuestServiceDetailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, pk):
        try:
            service = Service_Guide.objects.get(id=pk)
        except Service_Guide.DoesNotExist:
            return Response({"error": "Послугу не знайдено"}, status=404)

        serializer = GuestServiceDetailSerializer(service)
        return Response(serializer.data)
