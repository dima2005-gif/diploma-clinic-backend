from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response as DRFResponse

from main.models import Patient, Response
from main.serializers.patient.response_list.serializers import (
    PatientResponseListSerializer,
)


class PatientResponseListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            patient = Patient.objects.get(user=request.user)
        except Patient.DoesNotExist:
            return DRFResponse(
                {"error": "Профіль пацієнта не знайдено"},
                status=404,
            )

        responses = (
            Response.objects.select_related(
                "prescribed_service",
                "prescribed_service__service",
                "prescribed_service__doctor",
            )
            .filter(
                prescribed_service__patient=patient,
            )
            .order_by("-date_created")
        )

        serializer = PatientResponseListSerializer(responses, many=True)
        return DRFResponse(serializer.data)
