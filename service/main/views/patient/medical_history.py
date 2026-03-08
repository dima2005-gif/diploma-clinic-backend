from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from main.models import Medical_History, Patient
from main.serializers.patient.medical_history.serializers import (
    MedicalHistorySerializers,
)


class PatientMedicalHistoryListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            patient = Patient.objects.get(user=request.user)
            histories = (
                Medical_History.objects.select_related(
                    "prescribed_service__service", "diagnosis"
                )
                .filter(prescribed_service__patient=patient)
                .order_by("-prescribed_service__date_prescribed")
            )
            serializer = MedicalHistorySerializers(histories, many=True)
            return Response(serializer.data)
        except Patient.DoesNotExist:
            return Response({"error": "Пацієнта не знайдено"}, status=404)
