from datetime import datetime

from django.db.models import Count, Q
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from main.models import Employee


class DoctorVisitsStatisticsView(APIView):
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

        days_count = (end - start).days + 1

        doctors = (
            Employee.objects.filter(position__code__name="doctor")
            .annotate(
                total_visits=Count(
                    "prescribed_service",
                    filter=Q(
                        prescribed_service__date_prescribed__date__gte=start,
                        prescribed_service__date_prescribed__date__lte=end,
                        prescribed_service__status="Підтверджено",
                    ),
                )
            )
            .order_by("-total_visits")
        )

        total_visits_sum = sum(doctor.total_visits for doctor in doctors)

        data = []

        for doctor in doctors:
            popularity_percent = (
                round((doctor.total_visits / total_visits_sum) * 100, 2)
                if total_visits_sum
                else 0
            )
            data.append(
                {
                    "doctor_id": doctor.id,
                    "doctor": f"{doctor.last_name} {doctor.first_name} {doctor.middle_name}",
                    "position": doctor.position.name,
                    "total_visits": doctor.total_visits,
                    "average_per_day": round(doctor.total_visits / days_count, 2),
                    "popularity_percent": popularity_percent,
                }
            )

        return Response(
            {
                "start_date": start_date,
                "end_date": end_date,
                "days_count": days_count,
                "total_visits_sum": total_visits_sum,
                "status_filter": "Підтверджено",
                "results": data,
            }
        )
