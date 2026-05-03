from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from main.models import Employee, Prescribed_Service, Medical_History


class CloseMedicalHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        try:
            doctor = Employee.objects.get(user=request.user)
            service = Prescribed_Service.objects.get(id=pk, doctor=doctor)
            history = Medical_History.objects.get(prescribed_service=service)
        except (
            Employee.DoesNotExist,
            Prescribed_Service.DoesNotExist,
            Medical_History.DoesNotExist,
        ):
            return Response({"error": "Запис не знайдено"}, status=404)

        if history.date_departure:
            return Response({"error": "Історію вже закрито"}, status=400)

        history.date_departure = timezone.now().date()
        history.save()

        return Response({"message": "Історію хвороби закрито"})
