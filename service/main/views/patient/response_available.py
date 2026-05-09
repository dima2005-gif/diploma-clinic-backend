from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from main.models import Patient, Prescribed_Service
from main.serializers.patient.response_available.serializers import (
    PatientAvailableResponseSerializer,
)


class PatientAvailableResponseListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            patient = Patient.objects.get(user=request.user)
        except Patient.DoesNotExist:
            return Response({"error": "Профіль пацієнта не знайдено"}, status=404)

        services = (
            Prescribed_Service.objects.select_related(
                "doctor",
                "service",
                "medical_history",
            )
            .filter(
                patient=patient,
                status="Підтверджено",
                medical_history__date_departure__isnull=False,
            )
            .order_by("-date_prescribed")
        )

        serializer = PatientAvailableResponseSerializer(services, many=True)
        return Response(serializer.data)
