from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from main.models import Patient
from main.serializers.register.patient_list.serializers import (
    RegisterPatientListSerializer,
)


class RegisterPatientListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        patients = Patient.objects.all().order_by("id")

        serializer = RegisterPatientListSerializer(patients, many=True)

        return Response(serializer.data)
