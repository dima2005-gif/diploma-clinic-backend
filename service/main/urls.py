from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .auth.views import MyTokenObtainPairView, MyTokenRefreshView, LogoutView
from .views.patient.patient_dashboard import PatientDashboardView
from .views.patient.directory_services import DirectoryOfServicesView
from .views.patient.analysis_dashboard import PatientAnalysisView

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
]
