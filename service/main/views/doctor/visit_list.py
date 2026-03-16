from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from main.models import Employee, Prescribed_Service
from main.serializers.doctor.visit_list.serializers import DoctorVisitListSerializers


class DoctorVisitListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            doctor = Employee.objects.get(user=request.user)
        except Employee.DoesNotExist:
            return Response({"error": "Лікаря не знайдено"}, status=404)

        visits = Prescribed_Service.objects.filter(doctor=doctor).order_by(
            "date_prescribed"
        )
        serializer = DoctorVisitListSerializers(visits, many=True)
        return Response(serializer.data)
