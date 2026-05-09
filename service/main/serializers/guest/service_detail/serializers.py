from rest_framework import serializers

from main.models import Service_Guide, Position_Service, Employee, Work_Schedule


class GuestServiceDetailSerializer(serializers.ModelSerializer):
    positions = serializers.SerializerMethodField()
    doctors = serializers.SerializerMethodField()

    class Meta:
        model = Service_Guide
        fields = [
            "id",
            "name",
            "description",
            "price",
            "positions",
            "doctors",
        ]

    def get_positions(self, obj):
        relations = Position_Service.objects.select_related("position").filter(
            service=obj
        )

        return [
            {
                "id": relation.position.id,
                "name": relation.position.name,
            }
            for relation in relations
        ]

    def get_doctors(self, obj):
        position_ids = Position_Service.objects.filter(service=obj).values_list(
            "position_id", flat=True
        )

        doctors = Employee.objects.select_related("position", "user").filter(
            position_id__in=position_ids,
            user__is_active=True,
            date_of_dismissal__isnull=True,
        )

        result = []

        for doctor in doctors:
            schedule = Work_Schedule.objects.filter(employee=doctor).order_by("id")

            result.append(
                {
                    "id": doctor.id,
                    "full_name": (
                        f"{doctor.last_name} {doctor.first_name} {doctor.middle_name}"
                    ),
                    "position": doctor.position.name,
                    "schedule": [
                        {
                            "day_of_week": item.day_of_week,
                            "start_time": item.start_time,
                            "end_time": item.end_time,
                        }
                        for item in schedule
                    ],
                }
            )

        return result
