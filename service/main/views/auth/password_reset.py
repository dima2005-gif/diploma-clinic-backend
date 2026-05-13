from django.conf import settings
from django.core.mail import send_mail

from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from main.models import Patient, Employee
from main.serializers.auth.serializers import PasswordResetSerializer
from main.utils.password import generate_password


class PasswordResetView(APIView):
    permission_classes = [AllowAny]

    def find_profile_by_email(self, email):
        for patient in Patient.objects.select_related("user").all():
            if patient.email == email:
                return patient

        for employee in Employee.objects.select_related("user").all():
            if employee.email == email:
                return employee

        return None

    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        email = serializer.validated_data["email"]

        profile = self.find_profile_by_email(email)

        if profile is None:
            return Response(
                {"error": "Користувача з такою поштою не знайдено"},
                status=404,
            )

        user = profile.user

        if not user.is_active:
            return Response(
                {"error": "Обліковий запис заблоковано. Зверніться до адміністратора."},
                status=403,
            )

        new_password = generate_password()

        user.set_password(new_password)
        user.save()

        send_mail(
            subject="Відновлення доступу до eKarta",
            message=(
                "Для вашого облікового запису було згенеровано новий пароль.\n\n"
                f"Логін: {user.username}\n"
                f"Новий пароль: {new_password}\n\n"
                "Після входу збережіть нові дані доступу."
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=True,
        )

        return Response(
            {"message": "Дані для входу надіслано на електронну пошту"},
            status=200,
        )
