from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from main.models import Employee, Prescribed_Service
from main.serializers.doctor.visit_detail.serializers import DoctorVisitDetailSerializer


class DoctorVisitDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            doctor = Employee.objects.get(user=request.user)
            visit = Prescribed_Service.objects.get(id=pk, doctor=doctor)
        except (Employee.DoesNotExist, Prescribed_Service.DoesNotExist):
            return Response({"error": "Запис не знайдено"}, status=404)
        serializer = DoctorVisitDetailSerializer(visit)
        return Response(serializer.data)
