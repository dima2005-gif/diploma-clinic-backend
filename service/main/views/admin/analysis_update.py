from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from main.models import Analysis_Guide
from main.serializers.admin.analysis.serializers import AdminAnalysisSerializer


class AdminAnalysisUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        try:
            analysis = Analysis_Guide.objects.get(id=pk)
        except Analysis_Guide.DoesNotExist:
            return Response({"error": "Аналіз не знайдено"}, status=404)

        serializer = AdminAnalysisSerializer(
            analysis,
            data=request.data,
            partial=True,
        )

        if serializer.is_valid():
            serializer.save()

            return Response(
                {
                    "message": "Аналіз успішно оновлено",
                    "analysis": serializer.data,
                },
                status=200,
            )

        return Response(serializer.errors, status=400)
