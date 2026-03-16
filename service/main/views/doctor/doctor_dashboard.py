from rest_framework.views import APIView, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from main.models import Employee, Prescribed_Service
from datetime import datetime, timezone, timedelta


class DoctorDashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            doctor = Employee.objects.get(user=request.user)
        except Employee.DoesNotExist:
            return Response({"error": "Лікаря не знайдено"}, status=404)

        tz = timezone(timedelta(hours=2))
        now = datetime.now(tz)
        today = now.date()

        today_visits = Prescribed_Service.objects.filter(
            doctor=doctor, date_prescribed__date=today
        ).count()
        planned = Prescribed_Service.objects.filter(
            doctor=doctor, date_prescribed__date=today, status="Заплановано"
        ).count()
        confirmed = Prescribed_Service.objects.filter(
            doctor=doctor, date_prescribed__date=today, status="Підтверджено"
        ).count()
        next_visit = (
            Prescribed_Service.objects.filter(
                doctor=doctor,
                date_prescribed__gte=datetime.now(),
                status="Підтверджено",
            )
            .order_by("date_prescribed")
            .first()
        )

        return Response(
            {
                "name": f"{doctor.first_name} {doctor.last_name}",
                "today_count": today_visits,
                "planned_count": planned,
                "confirmed_count": confirmed,
                "next_visit": {
                    "time": next_visit.date_prescribed.strftime("%H:%M")
                    if next_visit
                    else None,
                    "patient": f"{next_visit.patient.first_name} {next_visit.patient.last_name}"
                    if next_visit
                    else None,
                },
            }
        )
