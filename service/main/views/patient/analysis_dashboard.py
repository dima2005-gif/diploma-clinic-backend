from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from main.models import Prescribed_Analysis, Patient
from main.serializers.patient.analysis_dashboard.serializers import (
    PrescribedAnalysisSerializers,
)


class PatientAnalysisView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            patient = Patient.objects.get(user=request.user)
            analyses = Prescribed_Analysis.objects.select_related(
                "medical_history__prescribed_service__doctor",
                "analysis",
            ).filter(medical_history__prescribed_service__patient=patient)
            serializer = PrescribedAnalysisSerializers(analyses, many=True)
            return Response(serializer.data)
        except Patient.DoesNotExist:
            return Response({"error": "Пацієнта не знайдено"}, status=404)
