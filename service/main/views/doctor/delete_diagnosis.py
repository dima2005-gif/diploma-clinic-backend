from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from main.models import Employee, Prescribed_Service, Medical_History


class DeleteDiagnosisView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
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

        history.diagnosis = None
        history.conclusion = ""
        history.save()

        return Response({"message": "Діагноз видалено"})
