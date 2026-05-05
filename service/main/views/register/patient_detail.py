from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from main.models import Patient
from main.serializers.register.patient_detail.serializers import (
    RegisterPatientDetailSerializer,
)


class RegisterPatientDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            patient = Patient.objects.select_related("user").get(id=pk)
        except Patient.DoesNotExist:
            return Response({"error": "Пацієнта не знайдено"}, status=404)

        serializer = RegisterPatientDetailSerializer(patient)

        return Response(serializer.data)
