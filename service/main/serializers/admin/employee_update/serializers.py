from datetime import date
from rest_framework import serializers
from main.models import Employee, Position


class AdminEmployeeUpdateSerializer(serializers.ModelSerializer):
    position_id = serializers.PrimaryKeyRelatedField(
        queryset=Position.objects.all(),
        source="position",
    )

    class Meta:
        model = Employee
        fields = [
            "first_name",
            "last_name",
            "middle_name",
            "position_id",
            "date_of_birth",
            "phone_number",
            "address",
            "email",
            "sex",
            "marital_status",
            "education",
            "date_of_hire",
        ]

    def validate_date_of_birth(self, value):
        if value > date.today():
            raise serializers.ValidationError(
                "Дата народження не може бути в майбутньому"
            )
        return value

    def validate_date_of_hire(self, value):
        if value > date.today():
            raise serializers.ValidationError("Дата найму не може бути в майбутньому")
        return value
