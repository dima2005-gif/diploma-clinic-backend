from rest_framework import serializers
from main.models import Prescribed_Service, Employee, Service_Guide


class ServiceGuideSerializers(serializers.ModelSerializer):
    class Meta:
        model = Service_Guide
        fields = ["name"]


class EmployeeSerializers(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ["first_name", "last_name", "middle_name"]


class PrescribedServiceSerializers(serializers.ModelSerializer):
    service = serializers.SerializerMethodField()
    doctor = serializers.SerializerMethodField()

    class Meta:
        model = Prescribed_Service
        fields = ["id", "service", "doctor", "date_prescribed", "status"]

    def get_service(self, obj):
        return ServiceGuideSerializers(obj.service).data

    def get_doctor(self, obj):
        return EmployeeSerializers(obj.doctor).data
