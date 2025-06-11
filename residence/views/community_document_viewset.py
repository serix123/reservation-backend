import os
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend

from core.filters import SmartSearchFilter
from residence.models import DocumentCategory, CommunityDocument
from residence.permissions import IsOfficer
from residence.serializers import (
    DocumentCategorySerializer,
    CommunityDocumentSerializer,
    CreateCommunityDocumentSerializer,
)


class CommunityDocumentViewSet(viewsets.ModelViewSet):
    queryset = CommunityDocument.objects.select_related("creator", "category").all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, OrderingFilter, SmartSearchFilter]
    filterset_fields = ["category", "creator"]
    search_fields = [
        "title",
        "description",
        "creator__username",
        "creator__email",
        "category__category_name",  # <<< Updated for new category_name field
    ]
    ordering_fields = ["created_at", "title", "category__category_name"]  # <<< Updated

    def get_serializer_class(self):
        if self.action == "create":
            return CreateCommunityDocumentSerializer
        return CommunityDocumentSerializer

    def create(self, request, *args, **kwargs):
        self.permission_classes = [IsOfficer]
        self.check_permissions(request)
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        self.permission_classes = [IsOfficer]
        self.check_permissions(request)

        # Before allowing the serializer to save, we need to handle the old file.
        # This instance is the object *before* the update.
        instance = self.get_object()
        old_id_document_path = None
        # Check if a new file is being uploaded for id_document AND an old one exists
        if "id_document" in request.FILES and instance.id_document:
            old_id_document_path = instance.id_document.path  # Store path before update

        # Let the super().update() method handle validation and saving, including the file.
        response = super().update(request, *args, **kwargs)

        # If the update was successful and a new file was uploaded, delete the old one.
        # This check is important because super().update() might not always save the file
        # if other validation errors occur.
        if (
            response.status_code in [status.HTTP_200_OK, status.HTTP_201_CREATED]
            and old_id_document_path
        ):
            import os
            from django.conf import settings

            # Ensure the old file path is within MEDIA_ROOT for safety
            if os.path.exists(old_id_document_path) and os.path.abspath(
                old_id_document_path
            ).startswith(os.path.abspath(settings.MEDIA_ROOT)):
                os.remove(old_id_document_path)

        return response

    def partial_update(self, request, *args, **kwargs):
        self.permission_classes = [IsOfficer]
        self.check_permissions(request)

        # Similar logic for partial updates
        instance = self.get_object()
        old_id_document_path = None
        if "id_document" in request.FILES and instance.id_document:
            old_id_document_path = instance.id_document.path

        response = super().partial_update(request, *args, **kwargs)

        if response.status_code in [status.HTTP_200_OK] and old_id_document_path:
            import os
            from django.conf import settings

            if os.path.exists(old_id_document_path) and os.path.abspath(
                old_id_document_path
            ).startswith(os.path.abspath(settings.MEDIA_ROOT)):
                os.remove(old_id_document_path)

        return response

    def destroy(self, request, *args, **kwargs):
        self.permission_classes = [IsOfficer]
        self.check_permissions(request)
        instance = self.get_object()
        # Delete associated file when patient is deleted
        if instance.id_document:
            instance.id_document.delete(save=False)
        return super().destroy(request, *args, **kwargs)

    @action(detail=True, methods=["put", "patch"], permission_classes=[IsOfficer])
    def upload_id_document(self, request, pk=None):
        """
        Dedicated endpoint for uploading/replacing ID document
        Endpoint: /documents/{pk}/upload_id_document/
        Methods: PUT (replace), PATCH (update)
        """
        document = self.get_object()

        if "id_document" not in request.FILES:
            return Response(
                {"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST
            )

        # Delete old file if exists
        if document.id_document:
            document.id_document.delete(save=False)

        # Save new file
        document.id_document = request.FILES["id_document"]
        document.save()

        serializer = self.get_serializer(document)
        return Response(serializer.data)


class DocumentCategoryViewSet(
    viewsets.ModelViewSet
):  # Changed to ModelViewSet for Officers to manage
    """
    API endpoint that allows Document Categories to be viewed, created, updated, or deleted.

    Permissions:
    - All Authenticated Users: Can view (list and retrieve).
    - Officers: Can create, update, and delete categories.
    """

    queryset = DocumentCategory.objects.all()
    serializer_class = DocumentCategorySerializer
    permission_classes = [
        IsAuthenticatedOrReadOnly
    ]  # Default: Read-only for authenticated

    filter_backends = [SmartSearchFilter, OrderingFilter, DjangoFilterBackend]
    search_fields = [
        "category_name",
        "parent__category_name",
    ]  # Search by category name and parent name
    ordering_fields = ["category_name"]

    # Override standard methods to apply Officer-specific permissions for write operations
    def create(self, request, *args, **kwargs):
        self.permission_classes = [IsOfficer]
        self.check_permissions(request)
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        self.permission_classes = [IsOfficer]
        self.check_permissions(request)
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        self.permission_classes = [IsOfficer]
        self.check_permissions(request)
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        self.permission_classes = [IsOfficer]
        self.check_permissions(request)
        return super().destroy(request, *args, **kwargs)

    @action(detail=True, methods=["put", "patch"], permission_classes=[IsOfficer])
    def upload_document(self, request, pk=None):
        """
        Dedicated endpoint for uploading/replacing ID document
        Endpoint: /documents/{pk}/upload_document/
        Methods: PUT (replace), PATCH (update)
        """
        document = self.get_object()

        if "id_document" not in request.FILES:
            return Response(
                {"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST
            )

        # Delete old file if exists
        if document.id_document:
            document.id_document.delete(save=False)

        # Save new file
        document.id_document = request.FILES["id_document"]
        document.save()

        serializer = self.get_serializer(document)
        return Response(serializer.data)
