from rest_framework import serializers
from main.models import Service_Guide


class AdminServiceListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service_Guide
        fields = [
            "id",
            "name",
        ]

