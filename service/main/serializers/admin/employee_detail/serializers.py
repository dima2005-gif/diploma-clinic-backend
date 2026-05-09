from rest_framework import serializers
from main.models import Employee


class AdminEmployeeDetailSerializer(serializers.ModelSerializer):
    login = serializers.CharField(source="user.username", read_only=True)
    is_active = serializers.BooleanField(source="user.is_active", read_only=True)
    is_current_user = serializers.SerializerMethodField()
    position = serializers.CharField(source="position.name", read_only=True)

    class Meta:
        model = Employee
        fields = [
            "id",
            "login",
            "first_name",
            "last_name",
            "middle_name",
            "date_of_birth",
            "phone_number",
            "address",
            "email",
            "sex",
            "marital_status",
            "education",
            "date_of_hire",
            "date_of_dismissal",
            "position",
            "is_active",
            "is_current_user",
        ]

    def get_is_current_user(self, obj):
        request = self.context.get("request")
        return bool(request and obj.user == request.user)

