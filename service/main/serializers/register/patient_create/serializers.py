from django.core.mail import send_mail
from django.conf import settings
from rest_framework import serializers

from main.models import CustomUser, Patient
from main.utils.username import generate_username
from main.utils.password import generate_password


class RegisterPatientCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = [
            "id",
            "first_name",
            "last_name",
            "middle_name",
            "date_of_birth",
            "phone_number",
            "email",
            "address",
            "sex",
            "weight",
            "height",
            "blood_group",
        ]

    def create(self, validated_data):
        email = validated_data["email"]

        username = generate_username(email)
        password = generate_password()

        user = CustomUser.objects.create(
            username=username,
            email=email,
            is_patient=True,
        )
        user.set_password(password)
        user.save()

        patient = Patient.objects.create(
            user=user,
            **validated_data,
        )

        send_mail(
            subject="Дані для входу в eKarta",
            message=(
                "Вас зареєстровано в системі eKarta.\n\n"
                f"Логін: {username}\n"
                f"Пароль: {password}\n\n"
                "Збережіть ці дані для входу."
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=True,
        )

        return patient
