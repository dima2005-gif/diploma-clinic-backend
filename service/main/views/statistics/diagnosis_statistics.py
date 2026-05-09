from datetime import datetime

from django.db.models import Count
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from main.models import Medical_History


class DiagnosisStatisticsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        start_date = request.query_params.get("start_date")
        end_date = request.query_params.get("end_date")

        if not start_date or not end_date:
            return Response(
                {"error": "Потрібно вказати дату початку та дату кінця"},
                status=400,
            )

        try:
            start = datetime.strptime(start_date, "%Y-%m-%d").date()
            end = datetime.strptime(end_date, "%Y-%m-%d").date()
        except ValueError:
            return Response(
                {"error": "Невірний формат дати. Використовуйте YYYY-MM-DD"},
                status=400,
            )

        if start > end:
            return Response(
                {"error": "Дата початку не може бути пізніше дати кінця"},
                status=400,
            )
        diagnoses = (
            Medical_History.objects.filter(
                prescribed_service__date_prescribed__date__gte=start,
                prescribed_service__date_prescribed__date__lte=end,
                diagnosis__isnull=False,
                date_departure__isnull=False,
            )
            .values(
                "diagnosis_id",
                "diagnosis__name",
            )
            .annotate(total_records=Count("id"))
            .order_by("-total_records")
        )

        total_diagnoses = sum(item["total_records"] for item in diagnoses)

        results = []

        for item in diagnoses:
            share_percent = (
                round((item["total_records"] / total_diagnoses) * 100, 2)
                if total_diagnoses > 0
                else 0
            )
            results.append(
                {
                    "diagnosis_id": item["diagnosis_id"],
                    "diagnosis": item["diagnosis__name"],
                    "total_records": item["total_records"],
                    "share_percent": share_percent,
                }
            )
        return Response(
            {
                "start_date": start_date,
                "end_date": end_date,
                "total_diagnoses": total_diagnoses,
                "results": results,
            }
        )
