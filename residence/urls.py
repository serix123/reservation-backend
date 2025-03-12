from django.urls import path, include
from rest_framework.routers import DefaultRouter
from residence.views import ResidenceViewSet

router = DefaultRouter()
router.register(r'residences', ResidenceViewSet, basename='residence')

urlpatterns = [
    path('', include(router.urls)),
]
