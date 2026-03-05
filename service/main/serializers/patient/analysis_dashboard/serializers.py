from rest_framework import serializers
from main.models import Analysis_Guide, Employee, Prescribed_Analysis


class AnalysisGuideSerializers(serializers.ModelSerializer):
    class Meta:
        model = Analysis_Guide
        fields = ["name"]


class EmployeeSerializers(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ["first_name", "last_name"]


class PrescribedAnalysisSerializers(serializers.ModelSerializer):
    analysis = AnalysisGuideSerializers(read_only=True)
    doctor = EmployeeSerializers(read_only=True)

    class Meta:
        model = Prescribed_Analysis
        fields = ["id", "analysis", "doctor", "date_prescribed", "status"]
