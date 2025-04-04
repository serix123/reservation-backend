from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response
from residence.models import Visitor, Residence
from residence.serializers import VisitorSerializer, CreateVisitorSerializer, SecurityCheckinSerializer
from residence.permissions import IsAdminOrOfficer, IsResidentOwner, SecurityStaffPermission
from authentication.models import User
from core.filters import SmartSearchFilter


class VisitorViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend,
                       SmartSearchFilter,  OrderingFilter]
    search_fields = [
        'name',
        'visit_purpose',
        'residence__user__email',
        'residence__address'
    ]

    def get_serializer_class(self):
        if self.action == 'security_checkin':
            return SecurityCheckinSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return CreateVisitorSerializer
        return VisitorSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Visitor.objects.all()
        return Visitor.objects.filter(residence__user=user)

    def perform_create(self, serializer):
        serializer.save(residence=self.request.user.residence)

    @action(detail=True, methods=['post'])
    def check_in(self, request, pk=None):
        visitor = self.get_object()

        if visitor.status != Visitor.VisitStatus.PENDING:
            return Response(
                {"error": "Visitor must be in pending status to check in"},
                status=status.HTTP_400_BAD_REQUEST  # This uses DRF's status codes
            )
        visitor.status = Visitor.VisitStatus.CHECKED_IN
        visitor.check_in_time = timezone.now()
        visitor.save()

        return Response(VisitorSerializer(visitor).data)

    @action(detail=True, methods=['post'])
    def check_out(self, request, pk=None):
        visitor = self.get_object()

        if visitor.status != Visitor.VisitStatus.CHECKED_IN:
            return Response(
                {"error": "Visitor must be checked in before checking out"},
                status=status.HTTP_400_BAD_REQUEST
            )

        visitor.status = Visitor.VisitStatus.CHECKED_OUT
        visitor.check_out_time = timezone.now()
        visitor.save()

        return Response(VisitorSerializer(visitor).data)

    @action(detail=False, methods=['get'])
    def current_visitors(self, request):
        """List all currently checked-in visitors"""
        queryset = self.filter_queryset(
            self.get_queryset().filter(status=Visitor.VisitStatus.CHECKED_IN)
        )
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'], url_path='security-checkin')
    def security_checkin(self, request):
        """
        Special endpoint for security staff to create visitors with auto check-in
        """
        # Check security staff permissions
        if not (request.user.is_staff and not request.user.is_superuser):
            return Response(
                {"error": "Only security staff can use this endpoint"},
                status=status.HTTP_403_FORBIDDEN
            )

        # Create visitor with auto check-in
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        visitor = serializer.save(
            resident=request.user.residence,
            status=Visitor.VisitStatus.CHECKED_IN,
            check_in_time=timezone.now()
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_permissions(self):
        # Only allow security staff to use the security-checkin endpoint
        if self.action == 'security_checkin':
            return [IsAuthenticated(), SecurityStaffPermission()]
        return super().get_permissions()
