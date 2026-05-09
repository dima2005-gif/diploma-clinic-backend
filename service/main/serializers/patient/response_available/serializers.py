from rest_framework import serializers
from main.models import Prescribed_Service, Response


class PatientAvailableResponseSerializer(serializers.ModelSerializer):
    service = serializers.CharField(source="service.name", read_only=True)
    doctor = serializers.SerializerMethodField()
    has_response = serializers.SerializerMethodField()

    class Meta:
        model = Prescribed_Service
        fields = [
            "id",
            "service",
            "doctor",
            "date_prescribed",
            "status",
            "has_response",
        ]

    def get_doctor(self, obj):
        return (
            f"{obj.doctor.last_name} {obj.doctor.first_name} {obj.doctor.middle_name}"
        )

    def get_has_response(self, obj):
        return Response.objects.filter(prescribed_service=obj).exists()
