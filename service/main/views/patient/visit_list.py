from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from main.models import Patient, Prescribed_Service
from main.serializers.patient.visit_list.serializers import PrescribedServiceSerializers
from main.views.patient import medical_history


class VisitListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            patient = Patient.objects.get(user=request.user)
            visits = (
                Prescribed_Service.objects.select_related(
                    "service",
                    "doctor",
                )
                .filter(patient=patient, medical_history__isnull=True)
                .order_by("-date_prescribed")
            )
            serializer = PrescribedServiceSerializers(visits, many=True)
            return Response(serializer.data)
        except Patient.DoesNotExist:
            return Response({"error": "Пацієнта не знайдено"}, status=404)
