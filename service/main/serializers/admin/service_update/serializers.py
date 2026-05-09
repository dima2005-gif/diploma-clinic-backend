from rest_framework import serializers
from main.models import Service_Guide, Position, Position_Service


class AdminServiceUpdateSerializer(serializers.ModelSerializer):
    position_ids = serializers.PrimaryKeyRelatedField(
        queryset=Position.objects.all(),
        many=True,
        write_only=True,
        required=False,
    )

    class Meta:
        model = Service_Guide
        fields = [
            "name",
            "description",
            "price",
            "position_ids",
        ]

    def update(self, instance, validated_data):
        positions = validated_data.pop("position_ids", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        if positions is not None:
            Position_Service.objects.filter(service=instance).delete()

            for position in positions:
                Position_Service.objects.create(
                    service=instance,
                    position=position,
                )

        return instance
