from django.db.models import Avg
from rest_framework import serializers

from main.models import Employee, Position_Service, Response, Work_Schedule


class GuestDoctorDetailSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    position = serializers.CharField(source="position.name", read_only=True)
    services = serializers.SerializerMethodField()
    schedule = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()
    reviews = serializers.SerializerMethodField()

    class Meta:
        model = Employee
        fields = [
            "id",
            "full_name",
            "position",
            "services",
            "schedule",
            "average_rating",
            "reviews",
        ]

    def get_full_name(self, obj):
        return f"{obj.last_name} {obj.first_name} {obj.middle_name}"

    def get_services(self, obj):
        relations = Position_Service.objects.select_related("service").filter(
            position=obj.position
        )

        return [
            {
                "id": relation.service.id,
                "name": relation.service.name,
                "price": relation.service.price,
            }
            for relation in relations
        ]

    def get_schedule(self, obj):
        schedule = Work_Schedule.objects.filter(employee=obj).order_by("id")

        return [
            {
                "day_of_week": item.day_of_week,
                "start_time": item.start_time,
                "end_time": item.end_time,
            }
            for item in schedule
        ]

    def get_average_rating(self, obj):
        rating = Response.objects.filter(prescribed_service__doctor=obj).aggregate(
            avg=Avg("rating")
        )["avg"]

        return round(rating, 2) if rating else None

    def get_reviews(self, obj):
        reviews = (
            Response.objects.select_related(
                "prescribed_service",
                "prescribed_service__patient",
                "prescribed_service__service",
            )
            .filter(prescribed_service__doctor=obj)
            .order_by("-date_created")
        )

        return [
            {
                "id": review.id,
                "patient": (
                    f"{review.prescribed_service.patient.last_name} "
                    f"{review.prescribed_service.patient.first_name}"
                ),
                "service": review.prescribed_service.service.name,
                "rating": review.rating,
                "comment": review.comment,
                "date_created": review.date_created,
            }
            for review in reviews
        ]
