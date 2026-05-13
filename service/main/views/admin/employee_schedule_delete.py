from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from main.models import Work_Schedule


class AdminEmployeeScheduleDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk, schedule_id):
        try:
            schedule = Work_Schedule.objects.get(
                id=schedule_id,
                employee_id=pk,
            )
        except Work_Schedule.DoesNotExist:
            return Response({"error": "Розклад не знайдено"}, status=404)

        schedule.delete()

        return Response({"message": "Розклад успішно видалено"}, status=200)
