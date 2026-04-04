from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from main.models import (
    Employee,
    Prescribed_Service,
    Medical_History,
    Prescribed_Medicine,
)


class DeleteMedicinesView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk, medicine_id):
        try:
            doctor = Employee.objects.get(user=request.user)
            service = Prescribed_Service.objects.get(id=pk, doctor=doctor)
            history = Medical_History.objects.get(prescribed_service=service)
            prescribed = Prescribed_Medicine.objects.get(
                id=medicine_id, medical_history=history
            )
        except (
            Employee.DoesNotExist,
            Prescribed_Service.DoesNotExist,
            Medical_History.DoesNotExist,
            Prescribed_Medicine.DoesNotExist,
        ):
            return Response({"error": "Запис не знайдено"}, status=404)

        prescribed.delete()

        return Response({"message": "Ліки видалено"})
