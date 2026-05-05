from datetime import date

from rest_framework import serializers

from main.models import Patient


class RegisterPatientUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = [
            "first_name",
            "last_name",
            "middle_name",
            "date_of_birth",
            "phone_number",
            "email",
            "address",
            "sex",
            "weight",
            "height",
            "blood_group",
        ]

    def validate_date_of_birth(self, value):
        if value > date.today():
            raise serializers.ValidationError(
                "Дата народження не може бути в майбутньому"
            )

        return value
