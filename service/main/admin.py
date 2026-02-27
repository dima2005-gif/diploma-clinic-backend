from django.contrib import admin
from .models import CustomUser, Position, Employee, Patient

admin.site.register(CustomUser)
admin.site.register(Position)
admin.site.register(Employee)
admin.site.register(Patient)

# Register your models here.
