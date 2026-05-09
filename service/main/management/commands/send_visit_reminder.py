from datetime import timedelta

from django.conf import settings
from django.core.mail import send_mail
from django.core.management.base import BaseCommand
from django.utils import timezone

from main.models import Prescribed_Service


class Command(BaseCommand):
    help = "Надсилання email-нагадувань про прийом за 3 дні"

    def handle(self, *args, **kwargs):
        target_date = timezone.now().date() + timedelta(days=3)

        visits = Prescribed_Service.objects.select_related(
            "patient",
            "doctor",
            "service",
        ).filter(
            status="Підтверджено",
            reminder_sent=False,
            date_prescribed__date=target_date,
        )

        for visit in visits:
            send_mail(
                subject="Нагадування про прийом в eKarta",
                message=(
                    "Нагадуємо, що у вас запланований прийом.\n\n"
                    f"Послуга: {visit.service.name}\n"
                    f"Лікар: {visit.doctor.last_name} {visit.doctor.first_name}\n"
                    f"Дата: {visit.date_prescribed.strftime('%d.%m.%Y %H:%M')}\n\n"
                    "Будь ласка, не забудьте прийти у зазначений час."
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[visit.patient.email],
                fail_silently=False,
            )

            visit.reminder_sent = True
            visit.save()

            self.stdout.write(
                self.style.SUCCESS(f"Нагадування надіслано для запису #{visit.id}")
            )
