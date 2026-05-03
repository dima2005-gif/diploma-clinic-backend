from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from main.models import Diagnosis_Guide
from main.serializers.doctor.diagnosis_list.serializers import DiagnosisListSerializers


class DiagnosisListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        diagnosis = Diagnosis_Guide.objects.all().order_by("name")
        serializer = DiagnosisListSerializers(diagnosis, many=True)
        return Response(serializer.data)
