from rest_framework import serializers
from main.models import Service_Guide


class GuestServiceListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service_Guide
        fields = [
            "id",
            "name",
            "description",
            "price",
        ]
