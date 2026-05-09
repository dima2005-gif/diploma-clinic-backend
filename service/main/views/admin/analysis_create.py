from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from main.serializers.admin.analysis.serializers import AdminAnalysisSerializer


class AdminAnalysisCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = AdminAnalysisSerializer(data=request.data)

        if serializer.is_valid():
            analysis = serializer.save()

            return Response(
                {
                    "message": "Аналіз успішно створено",
                    "id": analysis.id,
                },
                status=201,
            )

        return Response(serializer.errors, status=400)
