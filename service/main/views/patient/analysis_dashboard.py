from rest_framework import serializers
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
            analysis = (
                Prescribed_Analysis.objects.select_related("analysis", "doctor")
                .filter(patient=patient)
                .order_by("-date_prescribed")
            )
            serializer = PrescribedAnalysisSerializers(analysis, many=True)
            return Response(serializer.data)
        except Patient.DoesNotExist:
            return Response({"error": "Аналізи відсутні"}, status=404)
