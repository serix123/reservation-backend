from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly,
    IsAuthenticated,
)  # For read access
from rest_framework.response import Response
from django.conf import settings
from django_filters.rest_framework import DjangoFilterBackend
from core.filters import SmartSearchFilter
from residence.models import Notice
from residence.permissions import IsOfficer
from residence.serializers import NoticeSerializer


class NoticeViewSet(viewsets.ModelViewSet):
    queryset = Notice.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]

    # Add filter backends if you want to enable search, order, or filtering on notices
    filter_backends = [DjangoFilterBackend, OrderingFilter, SmartSearchFilter]
    search_fields = [
        "title",
        "details",
    ]
    ordering_fields = [
        "created_at",
        "title",
    ]

    serializer_class = NoticeSerializer

    def create(self, request, *args, **kwargs):
        # Override permissions to only allow Officers to create
        self.permission_classes = [IsOfficer]
        self.check_permissions(request)  # Crucial: forces the permission check
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        # Override permissions to only allow Officers to update
        self.permission_classes = [IsOfficer]
        self.check_permissions(request)

        # Handle file deletion for old image if a new one is uploaded
        instance = self.get_object()
        old_image_path = None
        if instance.image and "image" in request.FILES:
            old_image_path = instance.image.path

        # Let the serializer handle validation and saving, including the new image
        response = super().update(request, *args, **kwargs)

        # Safely delete the old image if a new one was uploaded successfully
        if response.status_code in [status.HTTP_200_OK] and old_image_path:
            if os.path.exists(old_image_path) and os.path.abspath(
                old_image_path
            ).startswith(os.path.abspath(settings.MEDIA_ROOT)):
                os.remove(old_image_path)

        return response

    def partial_update(self, request, *args, **kwargs):
        # Override permissions to only allow Officers to partial update
        self.permission_classes = [IsOfficer]
        self.check_permissions(request)

        # Handle file deletion for old image if a new one is uploaded during partial update
        instance = self.get_object()
        old_image_path = None
        if instance.image and "image" in request.FILES:
            old_image_path = instance.image.path

        response = super().partial_update(request, *args, **kwargs)

        if response.status_code in [status.HTTP_200_OK] and old_image_path:
            if os.path.exists(old_image_path) and os.path.abspath(
                old_image_path
            ).startswith(os.path.abspath(settings.MEDIA_ROOT)):
                os.remove(old_image_path)

        return response

    def destroy(self, request, *args, **kwargs):
        # Override permissions to only allow Officers to delete
        self.permission_classes = [IsOfficer]
        self.check_permissions(request)

        instance = self.get_object()
        # Delete associated image file when the notice is deleted
        if instance.image:
            instance.image.delete(
                save=False
            )  # delete(save=False) removes the file from storage

        return super().destroy(request, *args, **kwargs)

    @action(detail=True, methods=["put", "patch"], permission_classes=[IsAuthenticated])
    def upload(self, request, pk=None):
        """
        Dedicated endpoint for uploading/replacing ID notice
        Endpoint: /notices/{pk}/upload/
        Methods: PUT (replace), PATCH (update)
        """
        notice = self.get_object()

        if "image" not in request.FILES:
            return Response(
                {"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST
            )

        # Delete old file if exists
        if notice.image:
            notice.image.delete(save=False)

        # Save new file
        notice.image = request.FILES["image"]
        notice.save()

        serializer = self.get_serializer(notice)
        return Response(serializer.data)
