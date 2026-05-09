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
from .views.laboratory.laboratory_dashboard import LaborantDashboardView
from .views.laboratory.analysis_list import LaborantAnalysisListView
from .views.laboratory.analysis_confirm import LaborantAnalysisConfirmView
from .views.laboratory.analysis_detail import LaborantAnalysisDetailView
from .views.laboratory.analysis_update import LaborantAnalysisUpdateResultView
from .views.laboratory.analysis_delete import LaborantAnalysisDeleteResultView
from .views.register.patient_list import RegisterPatientListView
from .views.register.patient_detail import RegisterPatientDetailView
from .views.register.patient_create import RegisterPatientCreateView
from .views.register.patient_update import RegisterPatientUpdateView
from .views.admin.employee_list import AdminEmployeeListView
from .views.admin.employee_detail import AdminEmployeeDetailView
from .views.admin.position_list import AdminPositionListView
from .views.admin.employee_create import AdminEmployeeCreateView
from .views.admin.employee_update import AdminEmployeeUpdateView
from .views.admin.employee_deactivate import AdminEmployeeDeactivateView
from .views.admin.employee_activate import AdminEmployeeActivateView
from .views.admin.employee_schedule_list import AdminEmployeeScheduleView
from .views.admin.analysis_list import AdminAnalysisListView
from .views.admin.analysis_detail import AdminAnalysisDetailView
from .views.admin.analysis_create import AdminAnalysisCreateView
from .views.admin.analysis_update import AdminAnalysisUpdateView
from .views.admin.services_list import AdminServiceListView
from .views.admin.service_detail import AdminServiceDetailView
from .views.admin.service_create import AdminServiceCreateView
from .views.admin.service_update import AdminServiceUpdateView
from .views.admin.doctor_position import AdminDoctorPositionListView
from .views.admin.audit import AdminAuditView
from .views.statistics.doctor_visits import DoctorVisitsStatisticsView
from .views.statistics.service_popularity import ServicePopularityStatisticsView
from .views.statistics.analysis_popularity import AnalysisPopularityStatisticsView
from .views.statistics.diagnosis_statistics import DiagnosisStatisticsView
from .views.guest.service_list import GuestServiceListView
from .views.guest.service_detail import GuestServiceDetailView
from .views.guest.doctor_list import GuestDoctorListView
from .views.guest.doctor_detail import GuestDoctorDetailView
from .views.patient.response_create import PatientResponseCreateView
from .views.patient.response_available import PatientAvailableResponseListView
from .views.patient.response_list import PatientResponseListView
from .views.patient.response_update import PatientResponseUpdateView
from .views.auth.password_reset import PasswordResetView


urlpatterns = [
    path("login/", MyTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", MyTokenRefreshView.as_view(), name="token_refresh"),
    path("logout/", LogoutView.as_view(), name="auth_logout"),
    path("password-reset/", PasswordResetView.as_view(), name="password_reset"),
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
    path(
        "patient/response/create/",
        PatientResponseCreateView.as_view(),
        name="response_create",
    ),
    path("patient/response/available/", PatientAvailableResponseListView.as_view()),
    path("patient/responses/", PatientResponseListView.as_view()),
    path("patient/response/<int:pk>/update/", PatientResponseUpdateView.as_view()),
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
        "laborant-list/",
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
    # Laboratory
    path(
        "laborant/",
        LaborantDashboardView.as_view(),
        name="laborant_dashboard",
    ),
    path(
        "laborant/analysis/",
        LaborantAnalysisListView.as_view(),
        name="laborant_analysis",
    ),
    path(
        "laborant/analysis/<int:pk>/confirm/",
        LaborantAnalysisConfirmView.as_view(),
        name="laborant_analysis_confirm",
    ),
    path(
        "laborant/analysis/<int:pk>/",
        LaborantAnalysisDetailView.as_view(),
        name="laborant_analysis_detail",
    ),
    path(
        "laborant/analysis/<int:pk>/result/",
        LaborantAnalysisUpdateResultView.as_view(),
        name="laborant_analysis_result",
    ),
    path(
        "laborant/analysis/<int:pk>/result/delete/",
        LaborantAnalysisDeleteResultView.as_view(),
        name="laborant_analysis_cancel",
    ),
    # Register
    path("register/", RegisterPatientListView.as_view(), name="register"),
    path(
        "register/<int:pk>/",
        RegisterPatientDetailView.as_view(),
        name="register_detail",
    ),
    path(
        "register/create/", RegisterPatientCreateView.as_view(), name="register_create"
    ),
    path(
        "register/<int:pk>/update/",
        RegisterPatientUpdateView.as_view(),
        name="register_update",
    ),
    # Admin
    path(
        "admin/employee/", AdminEmployeeListView.as_view(), name="admin_employee_list"
    ),
    path(
        "admin/employee/<int:pk>/",
        AdminEmployeeDetailView.as_view(),
        name="admin_employee_detail",
    ),
    path(
        "admin/position/", AdminPositionListView.as_view(), name="admin_position_list"
    ),
    path(
        "admin/employee/create/", AdminEmployeeCreateView.as_view(), name="admin_create"
    ),
    path(
        "admin/employee/<int:pk>/update/",
        AdminEmployeeUpdateView.as_view(),
        name="admin_update",
    ),
    path(
        "admin/employee/<int:pk>/deactivate/",
        AdminEmployeeDeactivateView.as_view(),
        name="admin_deactivate",
    ),
    path(
        "admin/employee/<int:pk>/activate/",
        AdminEmployeeActivateView.as_view(),
        name="admin_activate",
    ),
    path(
        "admin/employee/<int:pk>/schedule/",
        AdminEmployeeScheduleView.as_view(),
        name="admin_schedule",
    ),
    path(
        "admin/analysis/", AdminAnalysisListView.as_view(), name="admin_analysis_list"
    ),
    path(
        "admin/analysis/<int:pk>/",
        AdminAnalysisDetailView.as_view(),
        name="admin_analysis_detail",
    ),
    path(
        "admin/analysis/create/", AdminAnalysisCreateView.as_view(), name="admin_create"
    ),
    path(
        "admin/analysis/<int:pk>/update/",
        AdminAnalysisUpdateView.as_view(),
        name="admin_update",
    ),
    path("admin/service/", AdminServiceListView.as_view(), name="admin_service_list"),
    path(
        "admin/service/<int:pk>/",
        AdminServiceDetailView.as_view(),
        name="admin_service",
    ),
    path(
        "admin/service/create/", AdminServiceCreateView.as_view(), name="admin_create"
    ),
    path(
        "admin/service/<int:pk>/update/",
        AdminServiceUpdateView.as_view(),
        name="admin_update",
    ),
    path(
        "admin/doctor-position/",
        AdminDoctorPositionListView.as_view(),
        name="admin_doctor_position",
    ),
    path("admin/audit/", AdminAuditView.as_view(), name="admin_audit"),
    path(
        "statistics/doctor-visits/",
        DoctorVisitsStatisticsView.as_view(),
        name="statistics_doctor_visits",
    ),
    path(
        "statistics/service-popularity/",
        ServicePopularityStatisticsView.as_view(),
        name="statistics_service_popularity",
    ),
    path(
        "statistics/analysis-popularity/",
        AnalysisPopularityStatisticsView.as_view(),
        name="statistics_analysis_popularity",
    ),
    path(
        "statistics/diagnosis/",
        DiagnosisStatisticsView.as_view(),
        name="statistics_diagnosis",
    ),
    # Guest
    path("guest/services/", GuestServiceListView.as_view(), name="guest_service_list"),
    path(
        "guest/services/<int:pk>/",
        GuestServiceDetailView.as_view(),
        name="guest_service_detail",
    ),
    path("guest/doctors/", GuestDoctorListView.as_view(), name="guest_doctor_list"),
    path(
        "guest/doctors/<int:pk>/", GuestDoctorDetailView.as_view(), name="guest_doctor"
    ),
]
