from django.contrib import admin
from .models import (
    CustomUser,
    Position,
    Employee,
    Patient,
    Service_Guide,
    Prescribed_Analysis,
    Analysis_Guide,
)

admin.site.register(CustomUser)
admin.site.register(Position)
admin.site.register(Employee)
admin.site.register(Patient)
admin.site.register(Service_Guide)
admin.site.register(Analysis_Guide)
admin.site.register(Prescribed_Analysis)

# Register your models here.
