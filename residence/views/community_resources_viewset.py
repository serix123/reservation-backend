# community/views.py
from authentication.permissions import IsAdminOrOfficer
from core.filters import SmartSearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions
from rest_framework.filters import OrderingFilter
from residence.models import CommunityResource
from residence.serializers import CommunityResourceSerializer


class CommunityResourceViewSet(viewsets.ModelViewSet):
    queryset = CommunityResource.objects.all()
    serializer_class = CommunityResourceSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrOfficer]
    filter_backends = [DjangoFilterBackend,
                       SmartSearchFilter,  OrderingFilter]
    filterset_fields = ['resource_type', 'status', ]
    search_fields = ['name', 'description', 'contact_info', 'managed_by__email',
                     'managed_by__first_name', 'managed_by__last_name']
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.IsAuthenticated()]
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(managed_by=self.request.user)
