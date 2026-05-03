from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils.dateparse import parse_datetime
from django.utils import timezone
from main.models import (
    Employee,
    Prescribed_Service,
    Medical_History,
    Analysis_Guide,
    Prescribed_Analysis,
)


class AddAnalysisView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            doctor = Employee.objects.get(user=request.user)
            service = Prescribed_Service.objects.get(id=pk, doctor=doctor)
        except (Employee.DoesNotExist, Prescribed_Service.DoesNotExist):
            return Response({"error": "Не знайдено"}, status=404)

        analysis_id = request.data.get("analysis_id")
        laboratory_assistant_id = request.data.get("laboratory_assistant_id")
        date_prescribed = request.data.get("date_prescribed")

        if not analysis_id or not laboratory_assistant_id or not date_prescribed:
            return Response(
                {"error": "Необхідно вказати аналіз, лаборанта та дату"},
                status=400,
            )

        try:
            analysis = Analysis_Guide.objects.get(id=analysis_id)
            laboratory_assistant = Employee.objects.get(
                id=laboratory_assistant_id,
                position__code__name="lab",
            )
        except Analysis_Guide.DoesNotExist:
            return Response({"error": "Аналіз не знайдено"}, status=404)
        except Employee.DoesNotExist:
            return Response({"error": "Лаборанта не знайдено"}, status=404)

        parsed_date = parse_datetime(date_prescribed)
        if not parsed_date:
            return Response({"error": "Некоректний формат дати"}, status=400)
        if parsed_date < timezone.now():
            return Response(
                {"error": "Неможливо призначити аналіз на минулу дату"},
                status=400,
            )

        history, _ = Medical_History.objects.get_or_create(prescribed_service=service)

        Prescribed_Analysis.objects.create(
            medical_history=history,
            analysis=analysis,
            laboratory_assistant=laboratory_assistant,
            date_prescribed=parsed_date,
            status="Заплановано",
        )

        return Response({"message": "Аналіз призначено"})
