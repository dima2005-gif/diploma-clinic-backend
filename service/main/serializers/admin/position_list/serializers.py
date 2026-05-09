from rest_framework import serializers
from main.models import Position


class AdminPositionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = [
            "id",
            "name",
        ]
