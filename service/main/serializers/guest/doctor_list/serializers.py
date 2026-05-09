from django.db.models import Avg
from rest_framework import serializers

from main.models import Employee, Response


class GuestDoctorListSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    position = serializers.CharField(source="position.name", read_only=True)
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = Employee
        fields = [
            "id",
            "full_name",
            "position",
            "average_rating",
        ]

    def get_full_name(self, obj):
        return f"{obj.last_name} {obj.first_name} {obj.middle_name}"

    def get_average_rating(self, obj):
        rating = Response.objects.filter(prescribed_service__doctor=obj).aggregate(
            avg=Avg("rating")
        )["avg"]

        return round(rating, 2) if rating else None
