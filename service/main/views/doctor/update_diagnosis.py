from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from main.models import Employee, Prescribed_Service, Medical_History, Diagnosis_Guide


class UpdateDiagnosisView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        try:
            doctor = Employee.objects.get(user=request.user)
            service = Prescribed_Service.objects.get(id=pk, doctor=doctor)
            history = Medical_History.objects.get(prescribed_service=service)
        except (
            Employee.DoesNotExist,
            Prescribed_Service.DoesNotExist,
            Medical_History.DoesNotExist,
        ):
            return Response({"error": "Запис не знайдено"}, status=404)

        diagnosis_id = request.data.get("diagnosis_id")
        conclusion = request.data.get("conclusion")

        if not diagnosis_id or not conclusion:
            return Response(
                {"error": "Необхідно вказати діагноз та висновок"}, status=404
            )

        diagnosis = Diagnosis_Guide.objects.get(id=diagnosis_id)
        history.diagnosis = diagnosis
        history.conclusion = conclusion
        history.save()

        return Response({"message": "Діагноз оновлено"})
