from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from main.models import Employee, Patient, Prescribed_Service
from main.serializers.patient.medical_history_detail.serializers import (
    MedicalHistoryDetailSerializers,
)


class PatientHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, patient_id):
        try:
            doctor = Employee.objects.get(user=request.user)
        except Employee.DoesNotExist:
            return Response({"error": "Лікаря не знайдено"}, status=404)

        patient = Patient.objects.filter(
            id=patient_id, prescribed_service__doctor=doctor
        ).first()

        if not patient:
            return Response({"error": "Пацієнта не знайдено"}, status=404)

        histories = (
            Prescribed_Service.objects.filter(patient=patient)
            .exclude(medical_history=None)
            .select_related(
                "medical_history__diagnosis",
                "doctor",
                "service",
            )
            .prefetch_related(
                "medical_history__prescribed_analysis_set__analysis",
                "medical_history__prescribed_analysis_set__laboratory_assistant",
                "medical_history__prescribed_medicine_set__medicine",
            )
        )

        data = MedicalHistoryDetailSerializers(
            [v.medical_history for v in histories], many=True
        ).data

        return Response(
            {
                "patient": {
                    "id": patient.id,
                    "first_name": patient.first_name,
                    "last_name": patient.last_name,
                    "middle_name": patient.middle_name,
                    "date_of_birth": patient.date_of_birth,
                    "phone_number": patient.phone_number,
                    "email": patient.email,
                },
                "histories": data,
            }
        )
