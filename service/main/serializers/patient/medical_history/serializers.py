from rest_framework import serializers
from main.models import Medical_History, Diagnosis_Guide


class DiagnosisGuideSerializers(serializers.ModelSerializer):
    class Meta:
        model = Diagnosis_Guide
        fields = ["name"]


class MedicalHistorySerializers(serializers.ModelSerializer):
    diagnosis = DiagnosisGuideSerializers(read_only=True)
    service = serializers.SerializerMethodField()
    date_arrival = serializers.SerializerMethodField()

    class Meta:
        model = Medical_History
        fields = ["id", "date_arrival", "date_departure", "service", "diagnosis"]

    def get_service(self, obj):
        return obj.prescribed_service.service.name

    def get_date_arrival(self, obj):
        return obj.prescribed_service.date_prescribed
