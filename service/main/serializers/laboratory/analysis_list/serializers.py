from rest_framework import serializers
from main.models import Prescribed_Analysis


class LaborantAnalysisListSerializer(serializers.ModelSerializer):
    patient = serializers.SerializerMethodField()
    doctor = serializers.SerializerMethodField()
    analysis = serializers.SerializerMethodField()
    result_url = serializers.SerializerMethodField()

    class Meta:
        model = Prescribed_Analysis
        fields = [
            "id",
            "patient",
            "doctor",
            "analysis",
            "date_prescribed",
            "status",
            "result_url",
        ]

    def get_patient(self, obj):
        patient = obj.medical_history.prescribed_service.patient

        return {
            "id": patient.id,
            "full_name": f"{patient.last_name} {patient.first_name} {patient.middle_name}",
        }

    def get_doctor(self, obj):
        doctor = obj.medical_history.prescribed_service.doctor

        return {
            "id": doctor.id,
            "full_name": f"{doctor.last_name} {doctor.first_name} {doctor.middle_name}",
        }

    def get_analysis(self, obj):
        return {
            "id": obj.analysis.id,
            "name": obj.analysis.name,
        }

    def get_result_url(self, obj):
        if obj.result:
            request = self.context.get("request")
            return request.build_absolute_uri(obj.result.url)

        return None
