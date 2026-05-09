from datetime import date

from django.core.mail import send_mail
from django.conf import settings
from rest_framework import serializers

from main.models import CustomUser, Employee, Position
from main.utils.password import generate_password
from main.utils.username import generate_username


class AdminEmployeeCreateSerializer(serializers.ModelSerializer):
    position_id = serializers.PrimaryKeyRelatedField(
        queryset=Position.objects.all(),
        source="position",
        write_only=True,
    )

    class Meta:
        model = Employee
        fields = [
            "id",
            "first_name",
            "last_name",
            "middle_name",
            "position_id",
            "date_of_birth",
            "phone_number",
            "address",
            "email",
            "sex",
            "marital_status",
            "education",
            "date_of_hire",
        ]

    def validate_date_of_birth(self, value):
        if value > date.today():
            raise serializers.ValidationError(
                "Дата народження не може бути в майбутньому"
            )
        return value

    def validate_date_of_hire(self, value):
        if value > date.today():
            raise serializers.ValidationError("Дата найму не може бути в майбутньому")
        return value

    def create(self, validated_data):
        email = validated_data["email"]
        username = generate_username(email)
        password = generate_password()

        user = CustomUser.objects.create(
            username=username,
            is_employee=True,
        )
        user.set_password(password)
        user.save()

        employee = Employee.objects.create(
            user=user,
            **validated_data,
        )

        send_mail(
            subject="Дані для входу в eKarta",
            message=(
                "Вас зареєстровано як співробітника в системі eKarta.\n\n"
                f"Логін: {username}\n"
                f"Пароль: {password}\n\n"
                "Збережіть ці дані для входу в систему."
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=False,
        )

        return employee
