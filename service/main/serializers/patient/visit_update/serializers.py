from rest_framework import serializers
from main.models import Prescribed_Service


class UpdatePrescribedServiceSerializers(serializers.ModelSerializer):
    class Meta:
        model = Prescribed_Service
        fields = ["service", "doctor", "date_prescribed"]
