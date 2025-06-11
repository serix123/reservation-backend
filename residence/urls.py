from django.urls import path, include
from rest_framework.routers import DefaultRouter
from residence.views import (
    ResidenceViewSet,
    VisitorViewSet,
    IssueViewSet,
    EventViewSet,
    CommunityResourceViewSet,
    IssueCommentViewSet,
    CommunityDocumentViewSet,
    DocumentCategoryViewSet,
    NoticeViewSet,
)

router = DefaultRouter()
router.register(r"categories", DocumentCategoryViewSet, basename="categories")
router.register(r"comments", IssueCommentViewSet, basename="comments")
router.register(r"documents", CommunityDocumentViewSet, basename="documents")
router.register(r"events", EventViewSet, basename="event")
router.register(r"issues", IssueViewSet, basename="issue")
router.register(r"notices", NoticeViewSet, basename="notices")
router.register(r"residences", ResidenceViewSet, basename="residence")
router.register(r"resources", CommunityResourceViewSet, basename="resource")
router.register(r"visitors", VisitorViewSet, basename="visitor")

urlpatterns = [
    path("", include(router.urls)),
]
