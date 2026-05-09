from rest_framework import serializers
from main.models import Work_Schedule


class AdminEmployeeScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Work_Schedule
        fields = [
            "id",
            "day_of_week",
            "start_time",
            "end_time",
        ]

    def validate(self, data):
        start_time = data.get("start_time", getattr(self.instance, "start_time", None))
        end_time = data.get("end_time", getattr(self.instance, "end_time", None))

        if start_time and end_time and start_time >= end_time:
            raise serializers.ValidationError(
                "Час початку має бути раніше часу завершення"
            )

        return data

