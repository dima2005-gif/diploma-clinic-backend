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
        start_time = data.get("start_time")
        end_time = data.get("end_time")

        if start_time and end_time and start_time >= end_time:
            raise serializers.ValidationError(
                {"end_time": "Час завершення має бути пізніше часу початку"}
            )

        return data
