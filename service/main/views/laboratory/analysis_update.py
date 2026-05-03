from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser

from main.models import Employee, Prescribed_Analysis


class LaborantAnalysisUpdateResultView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

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

        if analysis.status != "Підтверджено":
            return Response(
                {"error": "Результат можна додати лише для підтвердженого аналізу"},
                status=400,
            )

        result_file = request.FILES.get("result")

        if not result_file:
            return Response({"error": "Файл результату не передано"}, status=400)

        if result_file.content_type != "application/pdf":
            return Response({"error": "Можна завантажити лише PDF-файл"}, status=400)

        if analysis.result:
            analysis.result.delete(save=False)

        analysis.result = result_file
        analysis.save()

        return Response(
            {"message": "Результат аналізу успішно збережено"},
            status=200,
        )
