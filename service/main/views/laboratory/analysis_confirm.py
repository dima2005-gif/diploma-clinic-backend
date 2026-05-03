from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from main.models import Employee, Prescribed_Analysis


class LaborantAnalysisConfirmView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        try:
            laborant = Employee.objects.get(user=request.user)
        except Employee.DoesNotExist:
            return Response({"error": "Лаборанта не знайдено"}, status=404)

        try:
            analysis = Prescribed_Analysis.objects.get(
                id=pk,
                laboratory_assistant=laborant,
            )
        except Prescribed_Analysis.DoesNotExist:
            return Response({"error": "Аналіз не знайдено"}, status=404)

        if analysis.status != "Заплановано":
            return Response(
                {"error": "Можна змінити лише заплановані аналізи"},
                status=400,
            )

        action = request.data.get("action")

        if action == "confirm":
            analysis.status = "Підтверджено"
        elif action == "reject":
            analysis.status = "Відмовлено"
        else:
            return Response({"error": "Невірна дія"}, status=400)

        analysis.save()

        return Response(
            {"message": f"Статус змінено на '{analysis.status}'"},
            status=200,
        )

