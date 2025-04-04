from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import OrderingFilter

from core.filters import SmartSearchFilter
from residence.models import Residence
from residence.serializers import ResidenceSerializer, CreateResidenceSerializer, ResidenceUserSerializer


class ResidenceViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    filter_backends = [DjangoFilterBackend,
                       SmartSearchFilter,  OrderingFilter]
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
        elif self.action == 'profile':
            return ResidenceUserSerializer
        return ResidenceSerializer

    def get_queryset(self):
        # Admins can see all, regular users only their own
        if self.request.user.is_staff:
            return Residence.objects.all()
        return Residence.objects.filter(user=self.request.user)

    @action(detail=False, methods=['get'])
    def profile(self, request):
        """Handle current user's residence information"""
        try:
            residence = request.user.residence
        except Residence.DoesNotExist:
            return Response(
                {"detail": "No residence information found"},
                status=status.HTTP_404_NOT_FOUND
            )

        if request.method == 'GET':
            # Return combined user and residence data
            user_serializer = ResidenceUserSerializer(request.user)
            residence_serializer = self.get_serializer(residence)
            return Response({
                **user_serializer.data,
                **residence_serializer.data
            })

    def perform_create(self, serializer):
        # Automatically set first_name/last_name from user if not provided
        # user = self.request.user
        serializer.save(
            # first_name=serializer.validated_data.get(
            #     'first_name', user.first_name),
            # last_name=serializer.validated_data.get(
            #     'last_name', user.last_name)
        )
