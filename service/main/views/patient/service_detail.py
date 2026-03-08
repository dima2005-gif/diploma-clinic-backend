from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from main.models import Position_Service, Patient
from main.serializers.patient.service_detail.serializers import (
    PositionServiceSerializers,
)


class PatientServiceDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            patient = Patient.objects.get(user=request.user)
            service = Position_Service.objects.select_related(
                "service", "position"
            ).get(service__id=pk)
            serializer = PositionServiceSerializers(service)
            return Response(serializer.data)
        except Patient.DoesNotExist:
            return Response({"error": "Профіль пацієнта не знайдений"}, status=404)
        except Position_Service.DoesNotExist:
            return Response(
                {"error": "Послуга не знайдена або доступ заборонений"}, status=404
            )
