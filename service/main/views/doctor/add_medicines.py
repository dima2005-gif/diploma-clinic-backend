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


class AddMedicinesView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            doctor = Employee.objects.get(user=request.user)
            service = Prescribed_Service.objects.get(id=pk, doctor=doctor)
        except (Employee.DoesNotExist, Prescribed_Service.DoesNotExist):
            return Response({"error": "Не знайдено"}, status=404)

        medicine_id = request.data.get("medicine_id")
        recipe = request.data.get("recipe")

        if not medicine_id or not recipe:
            return Response({"error": "Необхідно вказати ліки та рецепт"}, status=404)

        medicine = Medicine_Guide.objects.get(id=medicine_id)
        history, _ = Medical_History.objects.get_or_create(prescribed_service=service)
        prescribed, created = Prescribed_Medicine.objects.get_or_create(
            medical_history=history,
            medicine=medicine,
            defaults={"recipe": recipe},
        )
        if not created:
            return Response({"error": "Ліки вже призначено змініть ліки"}, status=400)

        return Response({"message": "Ліки призначено"})
