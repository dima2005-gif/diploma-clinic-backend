from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from main.models import (
    Employee,
    Prescribed_Service,
    Medical_History,
    Prescribed_Analysis,
)


class CancelAnalysisView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk, analysis_id):
        try:
            doctor = Employee.objects.get(user=request.user)
            service = Prescribed_Service.objects.get(id=pk, doctor=doctor)
            history = Medical_History.objects.get(prescribed_service=service)
            prescribed_analysis = Prescribed_Analysis.objects.get(
                id=analysis_id,
                medical_history=history,
            )
        except (
            Employee.DoesNotExist,
            Prescribed_Service.DoesNotExist,
            Medical_History.DoesNotExist,
            Prescribed_Analysis.DoesNotExist,
        ):
            return Response({"error": "Запис не знайдено"}, status=404)

        if prescribed_analysis.status != "Заплановано":
            return Response(
                {"error": "Можна скасувати лише заплановані аналізи"},
                status=400,
            )

        prescribed_analysis.status = "Відмовлено"
        prescribed_analysis.save()

        return Response({"message": "Аналіз скасовано"})
