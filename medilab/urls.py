from django.urls import path, include
from rest_framework.routers import DefaultRouter
from medilab.views import PatientViewSet

router = DefaultRouter()
router.register(r"patients", PatientViewSet, basename="patient")


urlpatterns = [
    path("", include(router.urls)),
]
