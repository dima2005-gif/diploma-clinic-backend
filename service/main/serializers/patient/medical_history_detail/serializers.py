from rest_framework import serializers
from main.models import (
    Medical_History,
    Diagnosis_Guide,
    Employee,
    Prescribed_Analysis,
    Prescribed_Medicine,
    Analysis_Guide,
    Medicine_Guide,
)


class DiagnosisSerializers(serializers.ModelSerializer):
    class Meta:
        model = Diagnosis_Guide
        fields = ["name"]


class EmployeeSerializers(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ["id", "first_name", "last_name", "middle_name"]


class AnalysisGuideSerializers(serializers.ModelSerializer):
    class Meta:
        model = Analysis_Guide
        fields = ["name"]


class MedicineGuideSerializers(serializers.ModelSerializer):
    class Meta:
        model = Medicine_Guide
        fields = ["name"]


class PrescribedAnalysisSerializers(serializers.ModelSerializer):
    analysis = AnalysisGuideSerializers(read_only=True)
    laboratory_assistant = EmployeeSerializers(read_only=True)

    class Meta:
        model = Prescribed_Analysis
        fields = ["id", "analysis", "laboratory_assistant", "status", "result"]


class PrescribedMedicineSerializers(serializers.ModelSerializer):
    medicine = MedicineGuideSerializers(read_only=True)

    class Meta:
        model = Prescribed_Medicine
        fields = ["id", "medicine", "recipe"]


class MedicalHistoryDetailSerializers(serializers.ModelSerializer):
    diagnosis = DiagnosisSerializers(read_only=True)
    doctor = serializers.SerializerMethodField()
    service = serializers.SerializerMethodField()
    date_arrival = serializers.SerializerMethodField()
    analyses = PrescribedAnalysisSerializers(
        read_only=True, many=True, source="prescribed_analysis_set"
    )
    medicines = PrescribedMedicineSerializers(
        read_only=True, many=True, source="prescribed_medicine_set"
    )

    class Meta:
        model = Medical_History
        fields = [
            "id",
            "service",
            "date_arrival",
            "date_departure",
            "diagnosis",
            "doctor",
            "conclusion",
            "analyses",
            "medicines",
        ]

    def get_doctor(self, obj):
        return EmployeeSerializers(obj.prescribed_service.doctor).data

    def get_service(self, obj):
        return obj.prescribed_service.service.name

    def get_date_arrival(self, obj):
        return obj.prescribed_service.date_prescribed
