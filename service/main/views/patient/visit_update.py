from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from main.models import Patient, Prescribed_Service, Position_Service
from main.serializers.patient.visit_update.serializers import (
    UpdatePrescribedServiceSerializers,
)


class VisitUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        try:
            patient = Patient.objects.get(user=request.user)
        except Patient.DoesNotExist:
            return Response({"error": "Пацієнта не знайдено"}, status=404)

        try:
            visit = Prescribed_Service.objects.get(id=pk, patient=patient)
        except Prescribed_Service.DoesNotExist:
            return Response({"error": "Запис не знайдено"}, status=404)

        if visit.status != "Заплановано":
            return Response(
                {"error": "Можна редагувати лише заплановані записи"}, status=400
            )

        serializer = UpdatePrescribedServiceSerializers(visit, data=request.data)

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

        is_busy = (
            Prescribed_Service.objects.filter(
                doctor=doctor, date_prescribed=date_prescribed
            )
            .exclude(id=pk)
            .exists()
        )
        if is_busy:
            return Response({"error": "Цей час вже занятий"}, status=400)

        serializer.save()
        return Response(serializer.data)
