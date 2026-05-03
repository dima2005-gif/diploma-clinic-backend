from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from main.models import Employee
from main.serializers.doctor.lab_asistant.serializers import (
    LaboratoryAssistantListSerializer,
)


class LaboratoryAssistantListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        assistants = Employee.objects.filter(position__code__name="lab")
        serializer = LaboratoryAssistantListSerializer(assistants, many=True)
        return Response(serializer.data)
