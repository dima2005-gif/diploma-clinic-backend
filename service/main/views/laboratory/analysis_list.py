from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from main.models import Prescribed_Analysis
from main.serializers.laboratory.analysis_list.serializers import (
    LaborantAnalysisListSerializer,
)


class LaborantAnalysisListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        analyses = (
            Prescribed_Analysis.objects.select_related(
                "medical_history",
                "medical_history__prescribed_service",
                "medical_history__prescribed_service__patient",
                "medical_history__prescribed_service__doctor",
                "analysis",
                "laboratory_assistant",
            )
            .filter(laboratory_assistant__user=request.user)
            .order_by("-date_prescribed")
        )

        serializer = LaborantAnalysisListSerializer(
            analyses,
            many=True,
            context={"request": request},
        )

        return Response(serializer.data)
