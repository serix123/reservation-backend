from django.urls import path, include
from rest_framework.routers import DefaultRouter
from residence.views import ResidenceViewSet, VisitorViewSet, IssueViewSet, EventViewSet, CommunityResourceViewSet

router = DefaultRouter()
router.register(r'residences', ResidenceViewSet, basename='residence')
router.register(r'visitors', VisitorViewSet, basename='visitor')
router.register(r'issues', IssueViewSet, basename='issue')
router.register(r'events', EventViewSet, basename='event')
router.register(r'resources', CommunityResourceViewSet, basename='resource')

urlpatterns = [
    path('', include(router.urls)),
]
