from rest_framework import serializers
from main.models import Service_Guide, Position, Position_Service


class AdminServiceCreateSerializer(serializers.ModelSerializer):
    position_ids = serializers.PrimaryKeyRelatedField(
        queryset=Position.objects.all(),
        many=True,
        write_only=True,
    )

    class Meta:
        model = Service_Guide
        fields = [
            "id",
            "name",
            "description",
            "price",
            "position_ids",
        ]

    def create(self, validated_data):
        positions = validated_data.pop("position_ids")

        service = Service_Guide.objects.create(**validated_data)

        for position in positions:
            Position_Service.objects.create(
                service=service,
                position=position,
            )

        return service

