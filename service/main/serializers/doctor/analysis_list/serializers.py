from rest_framework import serializers
from main.models import Analysis_Guide


class AnalysisGuideListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Analysis_Guide
        fields = ["id", "name", "description", "price"]

