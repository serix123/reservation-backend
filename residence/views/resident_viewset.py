from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter, OrderingFilter

from residence.models import Residence
from residence.serializers import ResidenceSerializer, CreateResidenceSerializer


class ResidenceViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = [
        'first_name',
        'last_name',
        'role',
        'contact_number',
        'address'
    ]
    filterset_fields = ['role', 'registration_date']
    ordering_fields = [
        'registration_date',
        'first_name',
        'last_name'
    ]
    ordering = ['-registration_date']  # Default ordering

    def get_serializer_class(self):
        if self.action == 'create':
            return CreateResidenceSerializer
        return ResidenceSerializer

    def get_queryset(self):
        # Admins can see all, regular users only their own
        if self.request.user.is_staff:
            return Residence.objects.all()
        return Residence.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Automatically set first_name/last_name from user if not provided
        # user = self.request.user
        serializer.save(
            # first_name=serializer.validated_data.get(
            #     'first_name', user.first_name),
            # last_name=serializer.validated_data.get(
            #     'last_name', user.last_name)
        )
