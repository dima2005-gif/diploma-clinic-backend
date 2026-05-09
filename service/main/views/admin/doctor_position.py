from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from main.models import Position
from main.serializers.admin.position_list.serializers import (
    AdminPositionListSerializer,
)


class AdminDoctorPositionListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        positions = Position.objects.filter(
            code__name="doctor",
        ).order_by("name")

        serializer = AdminPositionListSerializer(positions, many=True)
        return Response(serializer.data)
