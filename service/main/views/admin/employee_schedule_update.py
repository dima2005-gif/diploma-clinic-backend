from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from main.models import Work_Schedule
from main.serializers.admin.schedule.serializers import (
    AdminEmployeeScheduleSerializer,
)


class AdminEmployeeScheduleUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk, schedule_id):
        try:
            schedule = Work_Schedule.objects.get(
                id=schedule_id,
                employee_id=pk,
            )
        except Work_Schedule.DoesNotExist:
            return Response({"error": "Розклад не знайдено"}, status=404)

        serializer = AdminEmployeeScheduleSerializer(
            schedule,
            data=request.data,
            partial=True,
        )

        if serializer.is_valid():
            serializer.save()

            return Response(
                {
                    "message": "Розклад успішно оновлено",
                    "schedule": serializer.data,
                },
                status=200,
            )

        return Response(serializer.errors, status=400)
