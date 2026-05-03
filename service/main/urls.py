from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .auth.views import MyTokenObtainPairView, MyTokenRefreshView, LogoutView
from .views.patient.patient_dashboard import PatientDashboardView
from .views.patient.directory_services import DirectoryOfServicesView
from .views.patient.analysis_dashboard import PatientAnalysisView
from .views.patient.analysis_detail import PatientAnalysisDetailView
from .views.patient.service_detail import PatientServiceDetailView
from .views.patient.medical_history import PatientMedicalHistoryListView
from .views.patient.medical_history_detail import PatientMedicalHistoryDetailView
from .views.patient.visit_list import VisitListView
from .views.appoinmemts import AvailableSlotView
from .views.patient.visit_create import VisitCreateView
from .views.patient.visit_update import VisitUpdateView
from .views.patient.visit_cancel import VisitCancelView
from .views.doctor.visit_confirm import VisitConfirmView
from .views.doctor.doctor_dashboard import DoctorDashboardView
from .views.doctor.visit_list import DoctorVisitListView
from .views.doctor.visit_detail import DoctorVisitDetailView
from .views.doctor.patient_history import PatientHistoryView
from .views.doctor.add_diagnosis import AddDiagnosisView
from .views.doctor.update_diagnosis import UpdateDiagnosisView
from .views.doctor.delete_diagnosis import DeleteDiagnosisView
from .views.doctor.add_medicines import AddMedicinesView
from .views.doctor.update_medicines import UpdateMedicinesView
from .views.doctor.delete_medicines import DeleteMedicinesView
from .views.doctor.diagnosis_list import DiagnosisListView
from .views.doctor.medicines_list import MedicinesListView
from .views.doctor.analysis_list import AnalysisGuideListView
from .views.doctor.lab_asistant_list import LaboratoryAssistantListView
from .views.doctor.add_analysis import AddAnalysisView
from .views.doctor.update_analysis import UpdateAnalysisView
from .views.doctor.delete_analysis import CancelAnalysisView
from .views.doctor.close_history import CloseMedicalHistoryView

urlpatterns = [
    path("login/", MyTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", MyTokenRefreshView.as_view(), name="token_refresh"),
    path("logout/", LogoutView.as_view(), name="auth_logout"),
    # Patient
    path("patient/", PatientDashboardView.as_view(), name="patient_dashboard"),
    path(
        "patient/services/", DirectoryOfServicesView.as_view(), name="patient_services"
    ),
    path("patient/analysis/", PatientAnalysisView.as_view(), name="patient_analysis"),
    path(
        "patient/analysis/<int:pk>/",
        PatientAnalysisDetailView.as_view(),
        name="patient_analysis_detail",
    ),
    path(
        "patient/services/<int:pk>/",
        PatientServiceDetailView.as_view(),
        name="patient_services_detail",
    ),
    path(
        "patient/medical-history/",
        PatientMedicalHistoryListView.as_view(),
        name="patient_medical_history",
    ),
    path(
        "patient/medical-history/<int:pk>/",
        PatientMedicalHistoryDetailView.as_view(),
        name="patient_medical_history_detail",
    ),
    path(
        "patient/visit/",
        VisitListView.as_view(),
        name="patient_visit_list",
    ),
    path(
        "patient/appointments/availble-slots/",
        AvailableSlotView.as_view(),
        name="slots",
    ),
    path(
        "patient/visit/create/",
        VisitCreateView.as_view(),
        name="patient_create_visit",
    ),
    path(
        "patient/visit/<int:pk>/update/",
        VisitUpdateView.as_view(),
        name="patient_update_visit",
    ),
    path(
        "patient/visit/<int:pk>/cancel/",
        VisitCancelView.as_view(),
        name="patient_cancel_visit",
    ),
    # Doctor
    path(
        "doctor/",
        DoctorDashboardView.as_view(),
        name="doctor_dashboard",
    ),
    path(
        "doctor/visit/<int:pk>/confirm/",
        VisitConfirmView.as_view(),
        name="doctor_confirm",
    ),
    path(
        "doctor/visit/",
        DoctorVisitListView.as_view(),
        name="doctor_visit_list",
    ),
    path(
        "doctor/visit/<int:pk>/",
        DoctorVisitDetailView.as_view(),
        name="doctor_visit_detail",
    ),
    path(
        "doctor/patient/<int:patient_id>/history/",
        PatientHistoryView.as_view(),
        name="doctor_patient_history",
    ),
    path(
        "doctor/visit/<int:pk>/add-diagnosis/",
        AddDiagnosisView.as_view(),
        name="doctor_add_diagnosis",
    ),
    path(
        "doctor/visit/<int:pk>/update-diagnosis/",
        UpdateDiagnosisView.as_view(),
        name="doctor_update_diagnosis",
    ),
    path(
        "doctor/visit/<int:pk>/delete-diagnosis/",
        DeleteDiagnosisView.as_view(),
        name="doctor_delete_diagnosis",
    ),
    path(
        "doctor/visit/<int:pk>/add-medicines/",
        AddMedicinesView.as_view(),
        name="doctor_add_medicines",
    ),
    path(
        "doctor/visit/<int:pk>/<medicine_id>/update-medicines/",
        UpdateMedicinesView.as_view(),
        name="doctor_update_medicines",
    ),
    path(
        "doctor/visit/<int:pk>/<medicine_id>/delete-medicines/",
        DeleteMedicinesView.as_view(),
        name="doctor_delete_medicines",
    ),
    path(
        "diagnosis/",
        DiagnosisListView.as_view(),
        name="doctor_diagnosis_list",
    ),
    path("medicines/", MedicinesListView.as_view(), name="doctor_medicines_list"),
    path("analysis/", AnalysisGuideListView.as_view(), name="doctor_analysis_list"),
    path(
        "laborant/",
        LaboratoryAssistantListView.as_view(),
        name="doctor_lab_asistant_list",
    ),
    path(
        "doctor/visit/<int:pk>/add-analysis/",
        AddAnalysisView.as_view(),
        name="doctor_add_analysis",
    ),
    path(
        "doctor/visit/<int:pk>/update-analysis/<analysis_id>/",
        UpdateAnalysisView.as_view(),
        name="doctor_update_analysis",
    ),
    path(
        "doctor/visit/<int:pk>/cancel-analysis/<analysis_id>/",
        CancelAnalysisView.as_view(),
        name="doctor_cancel_analysis",
    ),
    path(
        "doctor/visit/<int:pk>/close-history/",
        CloseMedicalHistoryView.as_view(),
        name="doctor_close_history",
    ),
]
