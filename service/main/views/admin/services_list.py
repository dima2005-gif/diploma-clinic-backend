from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from main.models import Service_Guide
from main.serializers.admin.service_list.serializers import (
    AdminServiceListSerializer,
)


class AdminServiceListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        services = Service_Guide.objects.all().order_by("id")

        serializer = AdminServiceListSerializer(
            services,
            many=True,
        )

        return Response(serializer.data)
