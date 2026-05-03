from rest_framework import serializers
from main.models import Medicine_Guide


class MedicinesListSerializers(serializers.ModelSerializer):
    class Meta:
        model = Medicine_Guide
        fields = ["id", "name"]
