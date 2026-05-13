from rest_framework import serializers
from main.models import Employee


class AdminEmployeeListSerializer(serializers.ModelSerializer):
    code = serializers.CharField(source="position.code.name", read_only=True)
    position = serializers.CharField(source="position.name", read_only=True)
    is_active = serializers.BooleanField(source="user.is_active", read_only=True)

    class Meta:
        model = Employee
        fields = [
            "id",
            "first_name",
            "last_name",
            "middle_name",
            "sex",
            "position",
            "date_of_hire",
            "date_of_dismissal",
            "is_active",
            "code",
        ]
