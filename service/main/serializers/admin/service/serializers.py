from rest_framework import serializers

from main.models import Service_Guide, Position_Service, Employee


class AdminServiceDetailSerializer(serializers.ModelSerializer):
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

        doctors = Employee.objects.select_related("position").filter(
            position_id__in=position_ids,
            date_of_dismissal__isnull=True,
            user__is_active=True,
        )

        return [
            {
                "id": doctor.id,
                "full_name": f"{doctor.last_name} {doctor.first_name} {doctor.middle_name}",
                "position": doctor.position.name,
            }
            for doctor in doctors
        ]
