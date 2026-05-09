from rest_framework import serializers
from main.models import Response


class PatientResponseListSerializer(serializers.ModelSerializer):
    service = serializers.CharField(
        source="prescribed_service.service.name",
        read_only=True,
    )
    doctor = serializers.SerializerMethodField()
    date_prescribed = serializers.DateTimeField(
        source="prescribed_service.date_prescribed",
        read_only=True,
    )

    class Meta:
        model = Response
        fields = [
            "id",
            "service",
            "doctor",
            "date_prescribed",
            "rating",
            "comment",
            "date_created",
        ]

    def get_doctor(self, obj):
        doctor = obj.prescribed_service.doctor
        return f"{doctor.last_name} {doctor.first_name} {doctor.middle_name}"
