from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Employee, Patient
from django.contrib.auth.models import Group


@receiver(post_save, sender=Employee)
def sync_employee_group(sender, instance, created, **kwargs):
    user = instance.user
    role_slug = instance.position.code

    user.is_employee = True
    user.is_patient = False

    if role_slug:
        group, _ = Group.objects.get_or_create(name=role_slug)
        user.groups.set([group])
    else:
        user.groups.clear()
    user.save()

@receiver(post_save, sender=Patient)
def sync_patient_group(sender, instance, created, **kwargs):
    user = instance.user
    user.is_patient = True
    user.is_employee = False

    group, _ = Group.objects.get_or_create(name='patient')
    user.groups.set([group])
    user.save()