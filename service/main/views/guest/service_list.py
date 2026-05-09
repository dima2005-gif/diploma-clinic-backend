from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from main.models import Service_Guide
from main.serializers.guest.service_list.serializers import (
    GuestServiceListSerializer,
)


class GuestServiceListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        services = Service_Guide.objects.all().order_by("name")
        serializer = GuestServiceListSerializer(services, many=True)
        return Response(serializer.data)
