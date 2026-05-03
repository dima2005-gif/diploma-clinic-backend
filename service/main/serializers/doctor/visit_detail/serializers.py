from rest_framework import serializers
from main.models import (
    Prescribed_Service,
    Patient,
    Medical_History,
    Diagnosis_Guide,
    Medicine_Guide,
    Prescribed_Medicine,
    Prescribed_Analysis,
    Analysis_Guide,
    Employee,
)


class MedicineGuideSerializers(serializers.ModelSerializer):
    class Meta:
        model = Medicine_Guide
        fields = ["id", "name"]


class PrescribedMedicineSerializers(serializers.ModelSerializer):
    medicine = MedicineGuideSerializers(read_only=True)

    class Meta:
        model = Prescribed_Medicine
        fields = ["id", "medicine", "recipe"]


class EmployeeSerializers(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ["id", "first_name", "last_name", "middle_name"]


class AnalysisSerializers(serializers.ModelSerializer):
    class Meta:
        model = Analysis_Guide
        fields = ["id", "name"]


class PrescribedAnalysisSerializers(serializers.ModelSerializer):
    analysis = AnalysisSerializers(read_only=True)
    laboratory_assistant = EmployeeSerializers(read_only=True)

    class Meta:
        model = Prescribed_Analysis
        fields = [
            "id",
            "analysis",
            "laboratory_assistant",
            "date_prescribed",
            "status",
            "result",
        ]


class MedicalHistorySerializer(serializers.ModelSerializer):
    diagnosis = serializers.StringRelatedField()
    medicines = PrescribedMedicineSerializers(
        many=True, read_only=True, source="prescribed_medicine_set"
    )
    analyses = PrescribedAnalysisSerializers(
        many=True, read_only=True, source="prescribed_analysis_set"
    )

    class Meta:
        model = Medical_History
        fields = [
            "id",
            "diagnosis",
            "conclusion",
            "medicines",
            "analyses",
            "date_departure",
        ]


class PatientDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = [
            "id",
            "first_name",
            "last_name",
            "middle_name",
            "date_of_birth",
            "sex",
            "phone_number",
            "email",
            "weight",
            "height",
            "blood_group",
        ]


class DoctorVisitDetailSerializer(serializers.ModelSerializer):
    patient = PatientDetailSerializer(read_only=True)
    service_name = serializers.CharField(source="service.name", read_only=True)
    history = MedicalHistorySerializer(read_only=True, source="medical_history")
    has_medical_history = serializers.SerializerMethodField()

    def get_has_medical_history(self, obj):
        return hasattr(obj, "medical_history")

    class Meta:
        model = Prescribed_Service
        fields = [
            "id",
            "patient",
            "service_name",
            "date_prescribed",
            "status",
            "has_medical_history",
            "history",
        ]
