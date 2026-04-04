from rest_framework import serializers
from main.models import Medical_History, Diagnosis_Guide


class AddDiagnosisSerializers(serializers.ModelSerializer):
    class Meta:
        model = Medical_History
        fields = ["prescribed_services", "diagnosis", "conclusion"]
