from rest_framework import serializers
from main.models import Prescribed_Service, Patient


class PatientSerializers(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ["id", "first_name", "last_name", "middle_name"]


class DoctorVisitListSerializers(serializers.ModelSerializer):
    patient = PatientSerializers(read_only=True)

    service_name = serializers.CharField(source="service.name", read_only=True)

    has_medical_history = serializers.SerializerMethodField()

    date_departure = serializers.SerializerMethodField()

    class Meta:
        model = Prescribed_Service

        fields = [
            "id",
            "patient",
            "service_name",
            "date_prescribed",
            "status",
            "has_medical_history",
            "date_departure",
        ]

    def get_has_medical_history(self, obj):
        return hasattr(obj, "medical_history")

    def get_date_departure(self, obj):
        if hasattr(obj, "medical_history"):
            return obj.medical_history.date_departure

        return None
