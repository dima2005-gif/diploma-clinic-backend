from rest_framework import serializers
from main.models import Patient


class RegisterPatientListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = [
            "id",
            "first_name",
            "last_name",
            "middle_name",
            "sex",
        ]
