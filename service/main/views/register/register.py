from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from main.models import Employee, Patient
from main.serializers.register.register.serializers import (
    RegisterDashboardSerializer,
)


class RegisterDashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            employee = Employee.objects.get(user=request.user)
        except Employee.DoesNotExist:
            return Response({"error": "Працівника не знайдено"}, status=404)

        serializer = RegisterDashboardSerializer(employee)

        data = serializer.data

        data["total_patients"] = Patient.objects.count()
        data["male_patients"] = Patient.objects.filter(sex="Чоловік").count()
        data["female_patients"] = Patient.objects.filter(sex="Жінка").count()

        return Response(data)

