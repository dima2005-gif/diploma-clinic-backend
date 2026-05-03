from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from main.models import Employee, Prescribed_Analysis
from datetime import datetime, timezone, timedelta


class LaborantDashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            laborant = Employee.objects.get(user=request.user)
        except Employee.DoesNotExist:
            return Response({"error": "Лаборанта не знайдено"}, status=404)

        tz = timezone(timedelta(hours=2))
        now = datetime.now(tz)
        today = now.date()

        today_analyses = Prescribed_Analysis.objects.filter(
            laboratory_assistant=laborant,
            date_prescribed__date=today,
        ).count()

        planned = Prescribed_Analysis.objects.filter(
            laboratory_assistant=laborant,
            date_prescribed__date=today,
            status="Заплановано",
        ).count()

        completed = Prescribed_Analysis.objects.filter(
            laboratory_assistant=laborant,
            date_prescribed__date=today,
            status="Виконано",
        ).count()

        next_analysis = (
            Prescribed_Analysis.objects.select_related(
                "analysis",
                "medical_history__prescribed_service__patient",
            )
            .filter(
                laboratory_assistant=laborant,
                date_prescribed__gte=now,
                status="Заплановано",
            )
            .order_by("date_prescribed")
            .first()
        )

        return Response(
            {
                "name": f"{laborant.first_name} {laborant.last_name}",
                "today_count": today_analyses,
                "planned_count": planned,
                "completed_count": completed,
                "next_analysis": {
                    "time": next_analysis.date_prescribed.strftime("%H:%M")
                    if next_analysis
                    else None,
                    "patient": (
                        f"{next_analysis.medical_history.prescribed_service.patient.first_name} "
                        f"{next_analysis.medical_history.prescribed_service.patient.last_name}"
                    )
                    if next_analysis
                    else None,
                    "analysis": next_analysis.analysis.name if next_analysis else None,
                },
            }
        )
