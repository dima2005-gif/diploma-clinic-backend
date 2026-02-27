from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from ...models import Patient
from ...serializers.patient.serializers import PatientDashboardSerializer

class PatientDashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            patient = Patient.objects.get(user=request.user)
            serializer = PatientDashboardSerializer(patient)
            return Response(serializer.data)
        except Patient.DoesNotExist:
            return Response({"error": "Профіль пацієнта не знайдений."}, status=404)