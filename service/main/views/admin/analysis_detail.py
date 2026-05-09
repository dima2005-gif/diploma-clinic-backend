from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from main.models import Analysis_Guide
from main.serializers.admin.analysis.serializers import (
    AdminAnalysisSerializer,
)


class AdminAnalysisDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            analysis = Analysis_Guide.objects.get(id=pk)
        except Analysis_Guide.DoesNotExist:
            return Response({"error": "Аналіз не знайдено"}, status=404)
        serializer = AdminAnalysisSerializer(analysis, many=False)
        return Response(serializer.data)
