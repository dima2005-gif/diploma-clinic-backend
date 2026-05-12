from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from main.models import Employee


class AdminDashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            admin = Employee.objects.get(user=request.user)
        except Employee.DoesNotExist:
            return Response({"error": "Адміністратора не знайдено"}, status=404)

        return Response(
            {
                "name": f"{admin.last_name} {admin.first_name} {admin.middle_name}",
                "position": admin.position.name if admin.position else "Адміністратор",
                "total_employees": Employee.objects.count(),
                "doctors_count": Employee.objects.filter(
                    position__code__name="doctor"
                ).count(),
                "laborants_count": Employee.objects.filter(
                    position__code__name="lab"
                ).count(),
                "registrars_count": Employee.objects.filter(
                    position__code__name="register"
                ).count(),
                "admins_count": Employee.objects.filter(
                    position__code__name="admin"
                ).count(),
            }
        )
