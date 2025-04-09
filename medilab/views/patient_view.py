from rest_framework import viewsets, permissions, status, serializers
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from core.filters import SmartSearchFilter
from django.contrib.auth import get_user_model
from medilab.models import PatientProfile, PatientProfileApplication
from medilab.serializers import (
    PatientProfileSerializer,
    PatientProfileApplicationSerializer,
    PatientProfileApplicationCreateSerializer,
    ApplicationReviewSerializer,
    PatientProfileUpdateSerializer,
)


User = get_user_model()


class PatientProfileViewSet(viewsets.ModelViewSet):
    """Viewset for approved patient profiles (read-only)"""

    queryset = PatientProfile.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [
        DjangoFilterBackend,
        SmartSearchFilter,
        OrderingFilter,
    ]
    search_fields = [
        "user__first_name",
        "user__last_name",
        "village",
        "address",
    ]
    ordering_fields = ["created_at", "approval_date"]
    ordering = ["-created_at"]  # Default ordering

    def get_queryset(self):
        queryset = PatientProfile.objects.all()
        if not self.request.user.is_staff:
            queryset = queryset.filter(user=self.request.user)
        return queryset

    # NEW SERIALIZER SELECTION:
    def get_serializer_class(self):
        if self.action in ["update", "partial_update"]:
            return PatientProfileUpdateSerializer  # Use special serializer for updates
        return PatientProfileSerializer

    def update(self, request, *args, **kwargs):
        """Handle profile updates by creating/modifying the single application"""
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        try:
            application = instance.create_update_application(serializer.validated_data)
            return Response(
                {
                    "detail": "Application updated successfully",
                    "application_id": application.id,
                    "status": application.status,
                    "is_update": application.is_update,
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def perform_create_application(self, instance, validated_data):
        """Helper method to create the update application"""
        instance.create_update_application(validated_data)


class PatientProfileApplicationViewSet(viewsets.ModelViewSet):
    """Viewset for profile applications"""

    queryset = PatientProfileApplication.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SmartSearchFilter, OrderingFilter]
    search_fields = [
        "user__first_name",
        "user__last_name",
        "village",
        "address",
        "status",
    ]
    filterset_fields = ["status", "is_update"]
    ordering_fields = ["created_at", "review_date"]
    ordering = ["-created_at"]  # Default ordering

    def get_serializer_class(self):
        if self.action == "create":
            return PatientProfileApplicationCreateSerializer
        elif self.action in ["approve", "reject"]:
            return ApplicationReviewSerializer
        return PatientProfileApplicationSerializer

    def perform_create(self, serializer):
        """Handle application creation ensuring single application per user"""
        if self.request.user.is_staff:
            raise permissions.PermissionDenied(
                "Staff cannot create profile applications"
            )

        # This will now either create or update the single application
        try:
            if hasattr(self.request.user, "patient_profile"):
                profile = self.request.user.patient_profile
                profile.create_update_application(serializer.validated_data)
            else:
                serializer.save(user=self.request.user, status="pending")
        except Exception as e:
            raise serializers.ValidationError(str(e))

    @action(
        detail=True, methods=["patch"], permission_classes=[permissions.IsAdminUser]
    )
    def approve(self, request, pk=None):
        """Staff-only action to approve an application"""
        application = self.get_object()
        if application.status != "pending":
            return Response(
                {"detail": "Only pending applications can be approved"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            application.approve(request.user)
            return Response(
                {"detail": "Application approved and archived"},
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(
        detail=True, methods=["patch"], permission_classes=[permissions.IsAdminUser]
    )
    def reject(self, request, pk=None):
        """Staff-only action to reject an application"""
        application = self.get_object()
        serializer = self.get_serializer(
            application,
            data={"status": "rejected"},
            partial=True,
            context={"request": request},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @action(detail=False, methods=["get"], permission_classes=[permissions.IsAdminUser])
    def pending(self, request):
        """List all pending applications (staff only)"""
        pending_apps = PatientProfileApplication.objects.filter(status="pending")
        serializer = self.get_serializer(pending_apps, many=True)
        return Response(serializer.data)

    # NEW ACTION ENDPOINT:
    @action(detail=False, methods=["get"])
    def my_updates(self, request):
        """New endpoint to view pending update requests"""
        if request.user.is_staff:
            queryset = PatientProfileApplication.objects.filter(
                is_update=True, status="pending"
            )
        else:
            queryset = PatientProfileApplication.objects.filter(
                user=request.user, is_update=True, status="pending"
            )

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
