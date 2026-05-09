from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response as DRFResponse

from main.models import Patient, Response
from main.serializers.patient.response_update.serializers import (
    PatientResponseUpdateSerializer,
)


class PatientResponseUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        try:
            patient = Patient.objects.get(user=request.user)
        except Patient.DoesNotExist:
            return DRFResponse(
                {"error": "Профіль пацієнта не знайдено"},
                status=404,
            )

        try:
            response = Response.objects.select_related(
                "prescribed_service",
                "prescribed_service__patient",
            ).get(
                id=pk,
                prescribed_service__patient=patient,
            )
        except Response.DoesNotExist:
            return DRFResponse(
                {"error": "Відгук не знайдено або він не належить пацієнту"},
                status=404,
            )

        serializer = PatientResponseUpdateSerializer(
            response,
            data=request.data,
            partial=True,
        )

        if serializer.is_valid():
            serializer.save()

            return DRFResponse(
                {
                    "message": "Відгук успішно оновлено",
                    "response": serializer.data,
                },
                status=200,
            )

        return DRFResponse(serializer.errors, status=400)
