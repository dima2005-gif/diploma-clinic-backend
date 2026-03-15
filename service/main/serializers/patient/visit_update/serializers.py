from rest_framework import serializers
from main.models import Prescribed_Service, Service_Guide, Employee


class ServiceShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service_Guide
        fields = ["id", "name"]


class DoctorShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ["id", "first_name", "last_name", "middle_name"]


class UpdatePrescribedServiceSerializers(serializers.ModelSerializer):
    service = ServiceShortSerializer(read_only=True)
    doctor = DoctorShortSerializer(read_only=True)
    service_id = serializers.PrimaryKeyRelatedField(
        queryset=Service_Guide.objects.all(), source="service", write_only=True
    )
    doctor_id = serializers.PrimaryKeyRelatedField(
        queryset=Employee.objects.all(), source="doctor", write_only=True
    )

    class Meta:
        model = Prescribed_Service
        fields = [
            "service",
            "doctor",
            "date_prescribed",
            "service_id",
            "doctor_id",
            "status",
        ]
        read_only_fields = ["status"]

