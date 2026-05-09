from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from main.models import Employee
from main.serializers.guest.doctor_list.serializers import (
    GuestDoctorListSerializer,
)


class GuestDoctorListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        doctors = (
            Employee.objects.select_related("position", "user")
            .filter(
                position__code__name="doctor",
                user__is_active=True,
                date_of_dismissal__isnull=True,
            )
            .order_by("last_name")
        )

        serializer = GuestDoctorListSerializer(doctors, many=True)
        return Response(serializer.data)
