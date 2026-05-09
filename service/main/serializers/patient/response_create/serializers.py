from rest_framework import serializers

from main.models import Response


class PatientResponseCreateSerializer(serializers.ModelSerializer):
    prescribed_service_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Response
        fields = [
            "id",
            "prescribed_service_id",
            "rating",
            "comment",
            "date_created",
        ]
        read_only_fields = [
            "id",
            "date_created",
        ]
