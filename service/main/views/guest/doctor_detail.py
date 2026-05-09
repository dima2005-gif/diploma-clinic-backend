from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from main.models import Employee
from main.serializers.guest.doctor_detail.serializers import (
    GuestDoctorDetailSerializer,
)


class GuestDoctorDetailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, pk):
        try:
            doctor = Employee.objects.select_related("position", "user").get(
                id=pk,
                position__code__name="doctor",
                user__is_active=True,
                date_of_dismissal__isnull=True,
            )
        except Employee.DoesNotExist:
            return Response({"error": "Лікаря не знайдено"}, status=404)

        serializer = GuestDoctorDetailSerializer(doctor)
        return Response(serializer.data)
