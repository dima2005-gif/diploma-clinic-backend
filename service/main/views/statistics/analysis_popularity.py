from datetime import datetime

from django.db.models import Count
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from main.models import Prescribed_Analysis


class AnalysisPopularityStatisticsView(APIView):
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

        analyses = (
            Prescribed_Analysis.objects.filter(
                date_prescribed__date__gte=start,
                date_prescribed__date__lte=end,
                status="Підтверджено",
            )
            .values(
                "analysis_id",
                "analysis__name",
            )
            .annotate(total_records=Count("id"))
            .order_by("-total_records")
        )

        total_analyses = sum(item["total_records"] for item in analyses)

        results = []
        for item in analyses:
            popularity_percent = (
                round((item["total_records"] / total_analyses) * 100, 2)
                if total_analyses
                else 0
            )

            results.append(
                {
                    "analysis_id": item["analysis_id"],
                    "analysis": item["analysis__name"],
                    "total_records": item["total_records"],
                    "popularity_percent": popularity_percent,
                }
            )

        return Response(
            {
                "start_date": start_date,
                "end_date": end_date,
                "total_analyses": total_analyses,
                "status_filter": "Підтверджено",
                "results": results,
            }
        )
