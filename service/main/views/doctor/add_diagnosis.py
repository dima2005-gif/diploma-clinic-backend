from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from main.models import Employee, Prescribed_Service, Medical_History, Diagnosis_Guide


class AddDiagnosisView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            doctor = Employee.objects.get(user=request.user)
            service = Prescribed_Service.objects.get(id=pk, doctor=doctor)
        except (Employee.DoesNotExist, Prescribed_Service.DoesNotExist):
            return Response({"error": "Не знайдено"}, status=404)
        diagnosis_id = request.data.get("diagnosis_id")
        conclusion = request.data.get("conclusion")

        if not diagnosis_id or not conclusion:
            return Response(
                {"error": "Необхідно вказати діагноз та висновок"}, status=404
            )

        diagnosis = Diagnosis_Guide.objects.get(id=diagnosis_id)
        history, created = Medical_History.objects.get_or_create(
            prescribed_service=service,
            defaults={"diagnosis": diagnosis, "conclusion": conclusion},
        )
        if not created:
            history.diagnosis = diagnosis
            history.conclusion = conclusion
            history.save()
            return Response({"message": "Діагноз вже було оновлено додано"})
        return Response({"message": "Діагноз додано"})
