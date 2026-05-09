from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from main.models import Analysis_Guide
from main.serializers.admin.analysis_list.serializers import AdminAnalysisListSerializer


class AdminAnalysisListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        analysis = Analysis_Guide.objects.all().order_by("id")
        serializer = AdminAnalysisListSerializer(analysis, many=True)
        return Response(serializer.data)
