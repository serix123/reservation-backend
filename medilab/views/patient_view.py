from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth import get_user_model
from core.filters import SmartSearchFilter
from medilab.models import Patient
from medilab.permissions import IsOwnerOrStaff
from medilab.serializers import PatientSerializer

User = get_user_model()


class PatientViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Patient model with custom actions for verification status management.
    """

    permission_classes = [permissions.IsAuthenticated, IsOwnerOrStaff]
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SmartSearchFilter, OrderingFilter]
    filterset_fields = [
        "verification_status",
        "gender",
    ]
    search_fields = [
        "first_name",
        "last_name",
        "address",
    ]

    def get_queryset(self):
        """
        Restrict queryset based on user permissions:
        - Staff users see all patients
        - Regular users only see their own patient profile
        """
        if self.request.user.is_staff:
            return Patient.objects.all()
        return Patient.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """Automatically associate the patient with the current user on creation."""
        serializer.save(user=self.request.user)

    def update(self, request, *args, **kwargs):
        """
        Handle patient updates with special handling for file uploads.
        - Prevents non-staff from modifying verification_status
        - Handles file deletion/replacement for id_document
        """
        partial = kwargs.pop("partial", False)
        instance = self.get_object()

        # Remove verification_status from data if user is not staff
        if not request.user.is_staff and "verification_status" in request.data:
            request.data.pop("verification_status")

        # Handle file upload
        id_document = request.FILES.get("id_document")
        if id_document:
            # Delete old file if exists
            if instance.id_document:
                instance.id_document.delete(save=False)
            instance.id_document = id_document
            # Automatically set status to pending when document is uploaded
            instance.verification_status = "pending"
            instance.save()

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        """Handle patient deletion with cleanup of associated files."""
        instance = self.get_object()
        # Delete associated file when patient is deleted
        if instance.id_document:
            instance.id_document.delete(save=False)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    # Custom actions for verification status management
    @action(detail=True, methods=["post"], permission_classes=[permissions.IsAdminUser])
    def verify(self, request, pk=None):
        """
        Custom action to mark patient as verified (staff only).
        Endpoint: /patients/{pk}/verify/
        """
        patient = self.get_object()
        patient.verification_status = "verified"
        patient.save()
        return Response({"status": "patient verified"})

    @action(detail=True, methods=["post"], permission_classes=[permissions.IsAdminUser])
    def reject(self, request, pk=None):
        """
        Custom action to mark patient as rejected (staff only).
        Endpoint: /patients/{pk}/reject/
        """
        patient = self.get_object()
        patient.verification_status = "rejected"
        patient.save()
        return Response({"status": "patient rejected"})

    @action(detail=True, methods=["post"], permission_classes=[permissions.IsAdminUser])
    def reset_verification(self, request, pk=None):
        """
        Custom action to reset verification status to pending (staff only).
        Endpoint: /patients/{pk}/reset_verification/
        """
        patient = self.get_object()
        patient.verification_status = "pending"
        patient.save()
        return Response({"status": "verification reset to pending"})

    @action(detail=False, methods=["get"], permission_classes=[permissions.IsAdminUser])
    def pending(self, request):
        """
        Custom action to list patients pending verification (staff only).
        Endpoint: /patients/pending/
        """
        pending_patients = Patient.objects.filter(verification_status="pending")
        serializer = self.get_serializer(pending_patients, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"], permission_classes=[permissions.IsAdminUser])
    def unverified(self, request):
        """
        Custom action to list patients unverified (staff only).
        Endpoint: /patients/unverified/
        """
        unverified_patients = Patient.objects.filter(verification_status="unverified")
        serializer = self.get_serializer(unverified_patients, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["put", "patch"], permission_classes=[IsOwnerOrStaff])
    def upload_id_document(self, request, pk=None):
        """
        Dedicated endpoint for uploading/replacing ID document
        Endpoint: /patients/{pk}/upload_id_document/
        Methods: PUT (replace), PATCH (update)
        """
        patient = self.get_object()

        if "id_document" not in request.FILES:
            return Response(
                {"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST
            )

        # Delete old file if exists
        if patient.id_document:
            patient.id_document.delete(save=False)

        # Save new file
        patient.id_document = request.FILES["id_document"]
        patient.save()

        serializer = self.get_serializer(patient)
        return Response(serializer.data)
