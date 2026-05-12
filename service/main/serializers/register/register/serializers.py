from rest_framework import serializers
from main.models import Employee


class RegisterDashboardSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    position = serializers.CharField(source="position.name", read_only=True)

    class Meta:
        model = Employee
        fields = ["name", "position"]

    def get_name(self, obj):
        return f"{obj.last_name} {obj.first_name} {obj.middle_name}"
