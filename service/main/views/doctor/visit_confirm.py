from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from main.models import Employee, Prescribed_Service


class VisitConfirmView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        try:
            doctor = Employee.objects.get(user=request.user)
        except Employee.DoesNotExist:
            return Response({"error": "Лікаря не знайдено"}, status=404)

        try:
            visit = Prescribed_Service.objects.get(id=pk, doctor=doctor)
        except Prescribed_Service.DoesNotExist:
            return Response({"error": "Запис не знайдено"}, status=404)

        if visit.status != "Заплановано":
            return Response(
                {"error": "Можна змінити лише заплановані записи"}, status=400
            )

        action = request.data.get("action")
        if action == "confirm":
            visit.status = "Підтверджено"
        elif action == "reject":
            visit.status = "Відмовлено"
        else:
            return Response({"error": "Невірна дія."}, status=400)

        visit.save()
        return Response({"message": f"Статус зміненно на '{visit.status}'"}, status=200)
