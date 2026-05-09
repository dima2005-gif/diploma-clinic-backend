from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response as DRFResponse

from main.models import (
    Patient,
    Prescribed_Service,
    Response,
)
from main.serializers.patient.response_create.serializers import (
    PatientResponseCreateSerializer,
)


class PatientResponseCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            patient = Patient.objects.get(user=request.user)
        except Patient.DoesNotExist:
            return DRFResponse(
                {"error": "Профіль пацієнта не знайдено"},
                status=404,
            )

        serializer = PatientResponseCreateSerializer(data=request.data)

        if not serializer.is_valid():
            return DRFResponse(serializer.errors, status=400)

        prescribed_service_id = serializer.validated_data["prescribed_service_id"]

        try:
            prescribed_service = Prescribed_Service.objects.select_related(
                "patient",
                "doctor",
                "service",
            ).get(
                id=prescribed_service_id,
                patient=patient,
            )
        except Prescribed_Service.DoesNotExist:
            return DRFResponse(
                {"error": "Прийом не знайдено або він не належить пацієнту"},
                status=404,
            )

        if prescribed_service.status != "Підтверджено":
            return DRFResponse(
                {"error": "Відгук можна залишити лише після підтвердженого прийому"},
                status=400,
            )

        if not hasattr(prescribed_service, "medical_history"):
            return DRFResponse(
                {"error": "Історію хвороби ще не створено"},
                status=400,
            )

        if prescribed_service.medical_history.date_departure is None:
            return DRFResponse(
                {"error": "Відгук можна залишити лише після закриття історії хвороби"},
                status=400,
            )

        if Response.objects.filter(prescribed_service=prescribed_service).exists():
            return DRFResponse(
                {"error": "Відгук для цього прийому вже залишено"},
                status=400,
            )

        response = Response.objects.create(
            prescribed_service=prescribed_service,
            rating=serializer.validated_data["rating"],
            comment=serializer.validated_data["comment"],
        )

        return DRFResponse(
            {
                "message": "Відгук успішно залишено",
                "id": response.id,
            },
            status=201,
        )
