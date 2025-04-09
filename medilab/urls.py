from django.urls import path, include
from rest_framework.routers import DefaultRouter
from medilab.views import PatientProfileViewSet, PatientProfileApplicationViewSet

router = DefaultRouter()
router.register(r"profiles", PatientProfileViewSet, basename="patient-profile")
router.register(
    r"applications", PatientProfileApplicationViewSet, basename="patient-application"
)

urlpatterns = [
    path("", include(router.urls)),
]
