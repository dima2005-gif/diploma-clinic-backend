from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from main.models import Service_Guide
from main.serializers.admin.service_update.serializers import (
    AdminServiceUpdateSerializer,
)


class AdminServiceUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        try:
            service = Service_Guide.objects.get(id=pk)
        except Service_Guide.DoesNotExist:
            return Response({"error": "Послугу не знайдено"}, status=404)

        serializer = AdminServiceUpdateSerializer(
            service,
            data=request.data,
            partial=True,
        )

        if serializer.is_valid():
            serializer.save()

            return Response(
                {"message": "Послугу успішно оновлено"},
                status=200,
            )

        return Response(serializer.errors, status=400)
