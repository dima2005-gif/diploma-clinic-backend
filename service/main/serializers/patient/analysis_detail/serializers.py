from rest_framework import serializers
from main.models import Prescribed_Analysis, Analysis_Guide, Employee


class AnalysisGuideSerializers(serializers.ModelSerializer):
    class Meta:
        model = Analysis_Guide
        fields = ["name", "description"]


class EmployeeSerializers(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ["first_name", "last_name", "middle_name"]


class PrescribedAnalysisViewSerializers(serializers.ModelSerializer):
    analysis = AnalysisGuideSerializers(read_only=True)
    doctor = serializers.SerializerMethodField()
    laboratory_assistant = EmployeeSerializers(read_only=True)
    date_prescribed = serializers.SerializerMethodField()

    class Meta:
        model = Prescribed_Analysis
        fields = [
            "id",
            "analysis",
            "doctor",
            "laboratory_assistant",
            "date_prescribed",
            "status",
            "result",
        ]

    def get_doctor(self, obj):
        doctor = obj.medical_history.prescribed_service.doctor
        return EmployeeSerializers(doctor).data

    def get_date_prescribed(self, obj):
        return obj.medical_history.prescribed_service.date_prescribed
