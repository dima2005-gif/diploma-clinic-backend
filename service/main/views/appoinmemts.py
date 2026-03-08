from datetime import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from main.models import Employee
from main.utils.appoinments import get_available_slots


class AvailableSlotView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        doctor_id = request.GET.get("doctor")
        date_str = request.GET.get("date")

        if not doctor_id or not date_str:
            return Response({"error": "Вкажіть лікаря і час"}, status=404)

        try:
            doctor = Employee.objects.get(id=doctor_id)
            date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except Employee.DoesNotExist:
            return Response({"error": "Лікаря не знайдено"}, status=404)
        except ValueError:
            return Response({"error": "Невірний формат дати"}, status=400)
        slots = get_available_slots(doctor, date)
        return Response({"slots": slots})
