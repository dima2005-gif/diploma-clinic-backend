from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from main.models import Employee, Prescribed_Analysis


class LaborantAnalysisDeleteResultView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
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

        if not analysis.result:
            return Response({"error": "Результат ще не додано"}, status=400)

        analysis.result.delete(save=False)
        analysis.result = None
        analysis.save()

        return Response(
            {"message": "Результат аналізу видалено"},
            status=200,
        )
