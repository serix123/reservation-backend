from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend

from core.filters import SmartSearchFilter
from residence.permissions import IsResident, IsOfficer, IsGuard
from residence.models import Issue, IssueComment
from residence.serializers import (
    IssueSerializer,
    CreateIssueSerializer,
    ResolveIssueSerializer,
    IssueCommentSerializer,
)


class IssueViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    filterset_fields = ["status", "priority", "assigned_to"]
    filter_backends = [SmartSearchFilter, DjangoFilterBackend, OrderingFilter]
    ordering_fields = ["-reported_date", "-resolved_date"]
    search_fields = ["title", "description"]
    queryset = Issue.objects.all()
    ordering = ["-reported_date", "-resolved_date"]

    def get_serializer_class(self):
        # if self.action == "create":
        #     return CreateIssueSerializer
        # if self.action == "resolve":
        #     return ResolveIssueSerializer
        return IssueSerializer

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return super().get_queryset().none()
        if IsGuard().has_permission(self.request, self) or IsOfficer().has_permission(
            self.request, self
        ):
            return super().get_queryset().exclude(status=Issue.IssueStatus.DRAFT)
        elif IsResident().has_permission(self.request, self):
            return super().get_queryset().filter(user=user)
        return super().get_queryset().none()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        self.permission_classes = [IsAuthenticated]
        self.check_permissions(request)
        instance = self.get_object()
        # Delete associated file when patient is deleted
        if instance.image:
            instance.image.delete(save=False)
        return super().destroy(request, *args, **kwargs)

    @action(detail=False, methods=["get"], permission_classes=[IsAuthenticated])
    def my_drafts(self, request):  # Action name changed for clarity
        """
        Retrieves a list of issues that are currently in 'draft' status
        and were reported by the current authenticated user.
        Accessible by any authenticated user.
        Endpoint: /api/issues/my_drafts/
        """
        user = request.user

        # Filter the queryset specifically for 'draft' issues AND the current authenticated user
        user_draft_issues = (
            self.get_queryset()
            .model.objects.filter(  # Access model directly to bypass get_queryset's default exclusion
                status=Issue.IssueStatus.DRAFT, user=user  # Filter by the current user
            )
            .order_by("-reported_date")
        )

        # Paginate the results
        page = self.paginate_queryset(user_draft_issues)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(user_draft_issues, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["post"])
    def resolve(self, request, pk=None):
        issue = self.get_object()

        issue.status = Issue.IssueStatus.RESOLVED
        issue.resolved_date = timezone.now()
        issue.save()

        return Response(IssueSerializer(issue).data)

    @action(detail=True, methods=["put", "patch"], permission_classes=[IsAuthenticated])
    def upload(self, request, pk=None):
        """
        Dedicated endpoint for uploading/replacing ID document
        Endpoint: /documents/{pk}/upload/
        Methods: PUT (replace), PATCH (update)
        """
        document = self.get_object()

        if "image" not in request.FILES:
            return Response(
                {"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST
            )

        # Delete old file if exists
        if document.image:
            document.image.delete(save=False)

        # Save new file
        document.image = request.FILES["image"]
        document.save()

        serializer = self.get_serializer(document)
        return Response(serializer.data)


class IssueCommentViewSet(viewsets.ModelViewSet):
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ["issue"]
    ordering_fields = ["-created_at"]
    queryset = IssueComment.objects.all()
    serializer_class = IssueCommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
