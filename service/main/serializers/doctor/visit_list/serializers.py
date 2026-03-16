from rest_framework import serializers
from main.models import Prescribed_Service, Patient


class PatientSerializers(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ["id", "first_name", "last_name", "middle_name"]


class DoctorVisitListSerializers(serializers.ModelSerializer):
    patient = PatientSerializers(read_only=True)
    service_name = serializers.CharField(source="service.name", read_only=True)

    class Meta:
        model = Prescribed_Service
        fields = ["id", "patient", "service_name", "date_prescribed", "status"]
