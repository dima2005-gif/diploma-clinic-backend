from rest_framework import serializers
from main.models import Patient
from datetime import date


class RegisterPatientDetailSerializer(serializers.ModelSerializer):
    login = serializers.CharField(source="user.username", read_only=True)
    age = serializers.SerializerMethodField()
    bmi = serializers.SerializerMethodField()

    class Meta:
        model = Patient
        fields = [
            "id",
            "login",
            "first_name",
            "last_name",
            "middle_name",
            "date_of_birth",
            "age",
            "phone_number",
            "email",
            "address",
            "sex",
            "weight",
            "height",
            "bmi",
            "blood_group",
        ]

    def get_age(self, obj):
        if obj.date_of_birth:
            today = date.today()
            return (
                today.year
                - obj.date_of_birth.year
                - (
                    (today.month, today.day)
                    < (obj.date_of_birth.month, obj.date_of_birth.day)
                )
            )
        return None

    def get_bmi(self, obj):
        if obj.weight and obj.height:
            height_in_meters = obj.height / 100
            bmi = obj.weight / (height_in_meters**2)
            return round(bmi, 2)
        return None
