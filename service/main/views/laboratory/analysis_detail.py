from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from main.models import Employee, Prescribed_Analysis
from main.serializers.laboratory.analysis_detail.serializers import (
    LaborantAnalysisDetailSerializer,
)


class LaborantAnalysisDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            laborant = Employee.objects.get(user=request.user)
        except Employee.DoesNotExist:
            return Response({"error": "Лаборанта не знайдено"}, status=404)

        try:
            analysis = Prescribed_Analysis.objects.select_related(
                "analysis",
                "laboratory_assistant",
                "medical_history",
                "medical_history__prescribed_service",
                "medical_history__prescribed_service__patient",
                "medical_history__prescribed_service__doctor",
            ).get(
                id=pk,
                laboratory_assistant=laborant,
            )
        except Prescribed_Analysis.DoesNotExist:
            return Response({"error": "Аналіз не знайдено"}, status=404)

        serializer = LaborantAnalysisDetailSerializer(
            analysis,
            context={"request": request},
        )

        return Response(serializer.data)
