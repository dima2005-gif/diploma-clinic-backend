from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from main.models import Analysis_Guide
from main.serializers.doctor.analysis_list.serializers import (
    AnalysisGuideListSerializer,
)


class AnalysisGuideListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        analyses = Analysis_Guide.objects.all()
        serializer = AnalysisGuideListSerializer(analyses, many=True)
        return Response(serializer.data)
