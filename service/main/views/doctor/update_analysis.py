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


class UpdateAnalysisView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk, analysis_id):
        try:
            doctor = Employee.objects.get(user=request.user)
            service = Prescribed_Service.objects.get(id=pk, doctor=doctor)
            history = Medical_History.objects.get(prescribed_service=service)
            prescribed_analysis = Prescribed_Analysis.objects.get(
                id=analysis_id,
                medical_history=history,
            )
        except (
            Employee.DoesNotExist,
            Prescribed_Service.DoesNotExist,
            Medical_History.DoesNotExist,
            Prescribed_Analysis.DoesNotExist,
        ):
            return Response({"error": "Запис не знайдено"}, status=404)

        if prescribed_analysis.status != "Заплановано":
            return Response(
                {"error": "Можна редагувати лише заплановані аналізи"},
                status=400,
            )

        new_analysis_id = request.data.get("analysis_id")
        laboratory_assistant_id = request.data.get("laboratory_assistant_id")
        date_prescribed = request.data.get("date_prescribed")

        if new_analysis_id:
            try:
                prescribed_analysis.analysis = Analysis_Guide.objects.get(
                    id=new_analysis_id
                )
            except Analysis_Guide.DoesNotExist:
                return Response({"error": "Аналіз не знайдено"}, status=404)

        if laboratory_assistant_id:
            try:
                prescribed_analysis.laboratory_assistant = Employee.objects.get(
                    id=laboratory_assistant_id,
                    position__code__name="lab",
                )
            except Employee.DoesNotExist:
                return Response({"error": "Лаборанта не знайдено"}, status=404)

        if date_prescribed:
            parsed_date = parse_datetime(date_prescribed)

            if not parsed_date:
                return Response({"error": "Неправильний формат дати"}, status=400)
            prescribed_analysis.date_prescribed = parsed_date
            if parsed_date < timezone.now():
                return Response(
                    {"error": "Дата не може бути меншою за поточну"},
                    status=400,
                )

        prescribed_analysis.save()

        return Response({"message": "Аналіз оновлено"})
