from django.contrib import admin
from .models import (
    CustomUser,
    Position,
    Employee,
    Patient,
    Service_Guide,
    Prescribed_Analysis,
    Analysis_Guide,
    Position_Service,
    Work_Schedule,
    Medical_History,
    Prescribed_Service,
    Prescribed_Medicine,
    Response,
    Diagnosis_Guide,
    Medicine_Guide,
    Code,
)

admin.site.register(CustomUser)
admin.site.register(Position)
admin.site.register(Employee)
admin.site.register(Patient)
admin.site.register(Service_Guide)
admin.site.register(Analysis_Guide)
admin.site.register(Prescribed_Analysis)
admin.site.register(Position_Service)
admin.site.register(Work_Schedule)
admin.site.register(Medical_History)
admin.site.register(Prescribed_Service)
admin.site.register(Prescribed_Medicine)
admin.site.register(Response)
admin.site.register(Diagnosis_Guide)
admin.site.register(Medicine_Guide)
admin.site.register(Code)

# Register your models here.
