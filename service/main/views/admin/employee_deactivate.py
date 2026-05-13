from datetime import date

from django.core.mail import send_mail
from django.conf import settings

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from main.models import Employee


class AdminEmployeeDeactivateView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        try:
            employee = Employee.objects.select_related("user").get(id=pk)
        except Employee.DoesNotExist:
            return Response({"error": "Співробітника не знайдено"}, status=404)

        if employee.user == request.user:
            return Response(
                {"error": "Ви не можете деактивувати власний акаунт"},
                status=400,
            )

        if not employee.user.is_active:
            return Response(
                {"error": "Співробітника вже деактивовано"},
                status=400,
            )

        dismissal_date = request.data.get("date_of_dismissal") or date.today()

        employee.date_of_dismissal = dismissal_date
        employee.user.is_active = False

        employee.user.save()
        employee.save()
        send_mail(
            subject="Зміна статусу акаунта eKarta",
            message=(
                "Ваш обліковий запис у системі eKarta було деактивовано.\n\n"
                "Якщо у вас виникли питання, зверніться до адміністратора."
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[employee.email],
            fail_silently=True,
        )

        return Response(
            {"message": "Співробітника успішно деактивовано"},
            status=200,
        )
