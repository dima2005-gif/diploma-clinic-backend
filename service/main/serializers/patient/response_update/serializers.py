from rest_framework import serializers
from main.models import Response


class PatientResponseUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Response
        fields = [
            "rating",
            "comment",
        ]
