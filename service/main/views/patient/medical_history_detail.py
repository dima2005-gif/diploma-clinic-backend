from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from main.models import Patient, Medical_History
from main.serializers.patient.medical_history_detail.serializers import (
    MedicalHistoryDetailSerializers,
)


class PatientMedicalHistoryDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            patient = Patient.objects.get(user=request.user)
            history = (
                Medical_History.objects.select_related(
                    "prescribed_service__doctor",
                    "prescribed_service__service",
                    "diagnosis",
                )
                .prefetch_related(
                    "prescribed_analysis_set__analysis",
                    "prescribed_analysis_set__laboratory_assistant",
                    "prescribed_medicine_set__medicine",
                )
                .get(id=pk, prescribed_service__patient=patient)
            )
            serializer = MedicalHistoryDetailSerializers(history)
            return Response(serializer.data)
        except Patient.DoesNotExist:
            return Response({"error": "Пацієнта не знайдено"}, status=404)
        except Medical_History.DoesNotExist:
            return Response({"error": "Історія не знайдена"}, status=404)
