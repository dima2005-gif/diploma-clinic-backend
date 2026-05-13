from django.core.mail import send_mail
from django.conf import settings

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from main.models import Employee


class AdminEmployeeActivateView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        try:
            employee = Employee.objects.select_related("user").get(id=pk)
        except Employee.DoesNotExist:
            return Response({"error": "Співробітника не знайдено"}, status=404)

        if employee.user.is_active:
            return Response(
                {"error": "Співробітника вже активовано"},
                status=400,
            )

        employee.user.is_active = True
        employee.date_of_dismissal = None

        employee.user.save()
        employee.save()

        send_mail(
            subject="Зміна статусу акаунта eKarta",
            message=(
                "Ваш обліковий запис у системі eKarta було активовано.\n\n"
                "Тепер ви можете знову увійти в систему."
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[employee.email],
            fail_silently=True,
        )

        return Response(
            {"message": "Співробітника успішно активовано"},
            status=200,
        )
