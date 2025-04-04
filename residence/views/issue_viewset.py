from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend

from core.filters import SmartSearchFilter
from residence.models import Issue
from residence.serializers import IssueSerializer, CreateIssueSerializer, ResolveIssueSerializer


class IssueViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    filterset_fields = ['status']
    filter_backends = [SmartSearchFilter, DjangoFilterBackend, OrderingFilter]
    ordering_fields = ['reported_date', 'resolved_date']
    search_fields = ['title', 'description']

    def get_serializer_class(self):
        if self.action == 'create':
            return CreateIssueSerializer
        if self.action == 'resolve':
            return ResolveIssueSerializer
        return IssueSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Issue.objects.all()
        return Issue.objects.filter(resident__user=user)

    def perform_create(self, serializer):
        serializer.save(resident=self.request.user.residence)

    @action(detail=True, methods=['post'])
    def resolve(self, request, pk=None):
        issue = self.get_object()

        if issue.status != Issue.IssueStatus.OPEN:
            return Response(
                {"error": "Only open issues can be resolved"},
                status=status.HTTP_400_BAD_REQUEST
            )

        issue.status = Issue.IssueStatus.RESOLVED
        issue.resolved_date = timezone.now()
        issue.save()

        return Response(IssueSerializer(issue).data)
