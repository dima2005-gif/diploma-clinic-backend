from rest_framework import serializers
from main.models import Diagnosis_Guide


class DiagnosisListSerializers(serializers.ModelSerializer):
    class Meta:
        model = Diagnosis_Guide
        fields = ["id", "name"]
