from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from main.models import Prescribed_Analysis, Patient
from main.serializers.patient.analysis_detail.serializers import (
    PrescribedAnalysisViewSerializers,
)


class PatientAnalysisDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            patient = Patient.objects.get(user=request.user)
            analysis = Prescribed_Analysis.objects.select_related(
                "medical_history__prescribed_service__doctor",
                "analysis",
                "laboratory_assistant",
            ).get(id=pk, medical_history__prescribed_service__patient=patient)
            serializer = PrescribedAnalysisViewSerializers(analysis)
            return Response(serializer.data)
        except Patient.DoesNotExist:
            return Response({"error": "Профіль пацієнта не знайдений"}, status=404)
        except Prescribed_Analysis.DoesNotExist:
            return Response(
                {"error": "Аналіз не знайдено або доступ заборонений"}, status=404
            )
