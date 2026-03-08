from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from main.serializers.patient.visit_create.serializers import (
    CreatePrescribedServiceSerializers,
)
from main.models import Patient, Prescribed_Service, Position_Service


class VisitCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            patient = Patient.objects.get(user=request.user)
        except Patient.DoesNotExist:
            return Response({"error": "Пацієнта не знайдено"}, status=404)
        serializer = CreatePrescribedServiceSerializers(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)
        doctor = serializer.validated_data["doctor"]
        date_prescribed = serializer.validated_data["date_prescribed"]
        service = serializer.validated_data["service"]

        is_valid = Position_Service.objects.filter(
            position=doctor.position, service=service
        ).exists()

        if not is_valid:
            return Response({"error": "Цей лікар не надає таку послугу"}, status=400)

        is_busy = Prescribed_Service.objects.filter(
            doctor=doctor, date_prescribed=date_prescribed
        ).exists()
        if is_busy:
            return Response({"error": "Цей час вже зайнятий"}, status=400)

        serializer.save(patient=patient, status="Заплановано")
        return Response(serializer.data, status=201)
