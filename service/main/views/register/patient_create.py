from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from main.serializers.register.patient_create.serializers import (
    RegisterPatientCreateSerializer,
)


class RegisterPatientCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = RegisterPatientCreateSerializer(data=request.data)

        if serializer.is_valid():
            patient = serializer.save()

            return Response(
                {
                    "message": "Пацієнта створено. Дані для входу надіслано на електронну пошту.",
                    "id": patient.id,
                    "login": patient.user.username,
                },
                status=201,
            )

        return Response(serializer.errors, status=400)
