from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from datetime import datetime

from main.models import (
    Patient,
    Employee,
    Position,
    Prescribed_Service,
    Medical_History,
    Prescribed_Analysis,
    Prescribed_Medicine,
    Response as PatientResponse,
)


class AdminAuditView(APIView):
    permission_classes = [IsAuthenticated]

    def get_action_label(self, history_type):
        actions = {
            "+": "Створення",
            "~": "Оновлення",
            "-": "Видалення",
        }
        return actions.get(history_type, "Невідома дія")

    def get_user_label(self, history_user):
        if history_user:
            return history_user.username
        return "Система / невідомо"

    def add_record(self, audit, record, model_name, object_label):
        audit.append(
            {
                "date": record.history_date,
                "user": self.get_user_label(record.history_user),
                "action": self.get_action_label(record.history_type),
                "model": model_name,
                "object": object_label,
            }
        )

    def get_person_label(self, record):
        return f"{record.last_name} {record.first_name} {record.middle_name}"

    def get_position_label(self, record):
        return record.name

    def get_prescribed_service_label(self, record):
        try:
            patient = record.patient
            service = record.service

            return (
                f"{patient.last_name} {patient.first_name} "
                f"{patient.middle_name} — {service.name}"
            )
        except Exception:
            return f"Прийом #{record.id}"

    def get_medical_history_label(self, record):
        try:
            patient = record.prescribed_service.patient
            return (
                f"Історія хвороби: {patient.last_name} "
                f"{patient.first_name} {patient.middle_name}"
            )
        except Exception:
            return f"Історія хвороби #{record.id}"

    def get_prescribed_analysis_label(self, record):
        try:
            patient = record.medical_history.prescribed_service.patient
            analysis = record.analysis

            return (
                f"{patient.last_name} {patient.first_name} "
                f"{patient.middle_name} — {analysis.name}"
            )
        except Exception:
            return f"Призначений аналіз #{record.id}"

    def get_prescribed_medicine_label(self, record):
        try:
            patient = record.medical_history.prescribed_service.patient
            medicine = record.medicine

            return (
                f"{patient.last_name} {patient.first_name} "
                f"{patient.middle_name} — {medicine.name}"
            )
        except Exception:
            return f"Призначені ліки #{record.id}"

    def get_response_label(self, record):
        try:
            patient = record.prescribed_service.patient
            doctor = record.prescribed_service.doctor

            return (
                f"Відгук: {patient.last_name} {patient.first_name} "
                f"→ {doctor.last_name} {doctor.first_name}"
            )
        except Exception:
            return f"Відгук #{record.id}"

    def get(self, request):
        audit = []

        for record in Patient.history.all():
            self.add_record(
                audit,
                record,
                "Пацієнт",
                self.get_person_label(record),
            )

        for record in Employee.history.all():
            self.add_record(
                audit,
                record,
                "Співробітник",
                self.get_person_label(record),
            )

        for record in Position.history.all():
            self.add_record(
                audit,
                record,
                "Посада",
                self.get_position_label(record),
            )

        for record in Prescribed_Service.history.all():
            self.add_record(
                audit,
                record,
                "Прийом",
                self.get_prescribed_service_label(record),
            )

        for record in Medical_History.history.all():
            self.add_record(
                audit,
                record,
                "Медична історія",
                self.get_medical_history_label(record),
            )

        for record in Prescribed_Analysis.history.all():
            self.add_record(
                audit,
                record,
                "Призначений аналіз",
                self.get_prescribed_analysis_label(record),
            )

        for record in Prescribed_Medicine.history.all():
            self.add_record(
                audit,
                record,
                "Призначені ліки",
                self.get_prescribed_medicine_label(record),
            )

        for record in PatientResponse.history.all():
            self.add_record(
                audit,
                record,
                "Відгук",
                self.get_response_label(record),
            )

        start_date = request.query_params.get("start_date")
        end_date = request.query_params.get("end_date")
        if start_date:
            start_date = datetime.strptime(start_date, "%Y-%m-%d").date()

            audit = [item for item in audit if item["date"].date() >= start_date]

        if end_date:
            end_date = datetime.strptime(end_date, "%Y-%m-%d").date()

            audit = [item for item in audit if item["date"].date() <= end_date]
        audit.sort(key=lambda item: item["date"], reverse=True)

        return Response(audit)
