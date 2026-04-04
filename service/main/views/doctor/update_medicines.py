from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from main.models import (
    Employee,
    Prescribed_Service,
    Medical_History,
    Medicine_Guide,
    Prescribed_Medicine,
)


class UpdateMedicinesView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk, medicine_id):
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

        new_medicine_id = request.data.get("medicine_id")
        new_recipe = request.data.get("recipe")

        if new_medicine_id:
            try:
                new_medicine = Medicine_Guide.objects.get(id=new_medicine_id)
                exists = (
                    Prescribed_Medicine.objects.filter(
                        medical_history=history, medicine=new_medicine
                    )
                    .exclude(id=medicine_id)
                    .exists()
                )
                if exists:
                    return Response({"error": "Такі ліки вже призначено"}, status=400)
                prescribed.medicine = new_medicine
            except Medicine_Guide.DoesNotExist:
                return Response({"error": "Ліки не знайдено"}, status=404)

        if new_recipe:
            prescribed.recipe = new_recipe

        prescribed.save()

        return Response({"message": "Ліки оновлено"})
