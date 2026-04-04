from rest_framework import serializers
from main.models import Prescribed_Service, Patient


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
        ]
