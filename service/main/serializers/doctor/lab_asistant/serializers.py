from rest_framework import serializers
from main.models import Employee


class LaboratoryAssistantListSerializer(serializers.ModelSerializer):
    position = serializers.CharField(source="position.name", read_only=True)

    class Meta:
        model = Employee
        fields = ["id", "first_name", "last_name", "middle_name", "position"]
