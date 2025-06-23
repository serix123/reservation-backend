from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from core.filters import SmartSearchFilter
from rest_framework import viewsets, status
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
    IsAdminUser,
)
from rest_framework.decorators import action
from rest_framework.response import Response
from residence.models import Event, Residence
from residence.permissions import IsOfficer, IsResident, CanViewAll
from residence.serializers import (
    EventSerializer,
    CreateEventSerializer,
    AttendEventSerializer,
    StatusUpdateSerializer,
)


class EventViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for viewing and editing Event instances.
    Includes actions for managing event attendance and filtering by time periods.
    """

    queryset = Event.objects.all()
    permission_classes = [
        IsAuthenticatedOrReadOnly
    ]  # Allow read for all, write for authenticated
    filterset_fields = ["creator", "date"]  # Added 'status' for filtering
    ordering_fields = [
        "-date",
        "-created_at",
        "-updated_at",
        "attendees_count",
    ]  # Added timestamps for ordering

    ordering = ["-date", "-updated_at", "-created_at"]

    filter_backends = [SmartSearchFilter, DjangoFilterBackend, OrderingFilter]
    search_fields = [
        "creator__first_name",
        "creator__last_name",
        "name",
        "location",
        "details",
    ]

    def get_serializer_class(self):
        """
        Returns the appropriate serializer class based on the action.
        """
        if self.action == "create":
            return CreateEventSerializer
        if self.action == "attend":
            return AttendEventSerializer
        if (
            self.action == "change_status"
        ):  # <-- New: Use StatusUpdateSerializer for this action
            return StatusUpdateSerializer
        # For list, retrieve, update, partial_update
        return EventSerializer

    def get_queryset(self):
        """
        Returns the queryset based on user roles and event status.
        """
        queryset = (
            Event.objects.select_related("creator").prefetch_related("attendees").all()
        )
        user = self.request.user

        if user.is_authenticated:
            return queryset
            # Users who can view all events (Officers, Superusers)
            # if CanViewAll().has_permission(self.request, self):
            #     return queryset
            # else:
            #     # Other authenticated users (Residents, Guards) see:
            #     # 1. Events they created (if any)
            #     # 2. Events with 'CONFIRMED' status
            #     return queryset.filter(
            #         Q(creator=user) | Q(status=Event.EventStatus.CONFIRMED)
            #     ).distinct()
        # else:
        #     # Unauthenticated users only see 'CONFIRMED' events
        #     return queryset.filter(status=Event.EventStatus.CONFIRMED)

    # Officer Permissions: Create
    def create(self, request, *args, **kwargs):
        # Override default create to apply IsOfficer permission
        self.permission_classes = [IsOfficer]
        self.check_permissions(request)
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        event = serializer.save(creator=self.request.user)
        event.attendees.add(self.request.user.residence)

    # Officer Permissions: Update (PATCH/PUT) and Delete
    def update(self, request, *args, **kwargs):
        self.permission_classes = [IsOfficer]
        self.check_permissions(request)
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        self.permission_classes = [IsOfficer]
        self.check_permissions(request)
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        self.permission_classes = [IsAuthenticated]
        self.check_permissions(request)
        instance = self.get_object()
        # Delete associated file when patient is deleted
        if instance.image:
            instance.image.delete(save=False)
        return super().destroy(request, *args, **kwargs)

    @action(
        detail=True, methods=["post"], permission_classes=[IsAuthenticatedOrReadOnly]
    )  # Officer can also attend
    def attend(self, request, pk=None):
        """
        Allows an authenticated Resident or Officer to attend or unattend an event.
        """
        event = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        action_type = serializer.validated_data["action"]
        user = request.user
        try:
            # Method 1: Directly access the related_name
            # This is the most common and direct way.
            residence_instance = user.residence

            # Method 2: If you want to be extra explicit or handle DoesNotExist gracefully
            # This is useful if the OneToOneField on Residence was nullable (which it isn't by default here)
            # or if you anticipate a User might not have a Residence profile yet for some reason.
            # residence_instance = Residence.objects.get(user=user)

        except Residence.DoesNotExist:
            return Response(
                {"detail": "Residence profile not found for this user."},
                status=status.HTTP_404_NOT_FOUND,
            )
        if action_type == "attend":
            if residence_instance not in event.attendees.all():
                event.attendees.add(residence_instance)
                message = "Successfully joined the event."
                status_code = status.HTTP_200_OK
            else:
                message = "You are already attending this event."
                status_code = status.HTTP_409_CONFLICT
        elif action_type == "unattend":
            if residence_instance in event.attendees.all():
                event.attendees.remove(residence_instance)
                message = "Successfully unjoined the event."
                status_code = status.HTTP_200_OK
            else:
                message = "You are not attending this event."
                status_code = status.HTTP_409_CONFLICT

        event.refresh_from_db()

        return Response(
            EventSerializer(event, context={"request": request}).data,
            status=status_code,
        )

    # Officer Permissions: Change Status
    @action(detail=True, methods=["post"], permission_classes=[IsOfficer])
    def change_status(self, request, pk=None):
        """
        Allows an admin/superuser to change the status of an event to CONFIRMED or REJECTED.
        Access is restricted to IsAdminUser (superusers).
        """
        event = self.get_object()  # Get the specific event
        serializer = self.get_serializer(
            data=request.data
        )  # Use StatusUpdateSerializer
        serializer.is_valid(raise_exception=True)

        # new_status = serializer.validated_data["status"]

        # # Optional: Add specific business logic for transitions if needed
        # # For example, prevent re-confirming an already confirmed event, etc.
        # if event.status == new_status:
        #     return Response(
        #         {"detail": f"Event is already {new_status}."},
        #         status=status.HTTP_409_CONFLICT,
        #     )
        # if (
        #     new_status == Event.EventStatus.CONFIRMED
        #     and event.status == Event.EventStatus.REJECTED
        # ):
        #     return Response(
        #         {"detail": "Cannot confirm a rejected event directly."},
        #         status=status.HTTP_400_BAD_REQUEST,
        #     )

        event.status = new_status
        event.save()  # This will automatically update 'updated_at'

        # Return the full event data with the updated status
        return Response(
            EventSerializer(event, context={"request": request}).data,
            status=status.HTTP_200_OK,
        )

    @action(detail=False, methods=["get"])
    def upcoming(self, request):
        """
        Retrieves upcoming events (from now onwards).
        Applies general visibility rules from get_queryset.
        """
        # The get_queryset() call already applies the user-specific visibility logic
        queryset = self.filter_queryset(
            self.get_queryset().filter(date__gte=timezone.now())
        ).order_by("date")

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def past(self, request):
        """
        Retrieves past events (before now).
        Applies general visibility rules from get_queryset.
        """
        queryset = self.filter_queryset(
            self.get_queryset().filter(date__lt=timezone.now())
        ).order_by("-date")

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def ongoing_this_month(self, request):
        """
        Retrieves events ongoing this month (from the 1st of the current month to its end).
        Applies general visibility rules from get_queryset.
        """
        now = timezone.now()
        start_of_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

        # Calculate end of month correctly
        if now.month == 12:
            end_of_month = now.replace(
                year=now.year + 1,
                month=1,
                day=1,
                hour=0,
                minute=0,
                second=0,
                microsecond=0,
            ) - timezone.timedelta(microseconds=1)
        else:
            end_of_month = now.replace(
                month=now.month + 1, day=1, hour=0, minute=0, second=0, microsecond=0
            ) - timezone.timedelta(microseconds=1)

        queryset = self.filter_queryset(
            self.get_queryset().filter(date__range=(start_of_month, end_of_month))
        ).order_by("date")

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def upcoming_next_month(self, request):
        """
        Retrieves events scheduled for next month onwards.
        Applies general visibility rules from get_queryset.
        """
        now = timezone.now()
        # Calculate the first day of next month
        if now.month == 12:
            start_of_next_month = now.replace(
                year=now.year + 1,
                month=1,
                day=1,
                hour=0,
                minute=0,
                second=0,
                microsecond=0,
            )
        else:
            start_of_next_month = now.replace(
                month=now.month + 1, day=1, hour=0, minute=0, second=0, microsecond=0
            )

        queryset = self.filter_queryset(
            self.get_queryset().filter(date__gte=start_of_next_month)
        ).order_by("date")

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["put", "patch"], permission_classes=[IsAuthenticated])
    def upload(self, request, pk=None):
        """
        Dedicated endpoint for uploading/replacing ID event
        Endpoint: /events/{pk}/upload/
        Methods: PUT (replace), PATCH (update)
        """
        event = self.get_object()

        if "image" not in request.FILES:
            return Response(
                {"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST
            )

        # Delete old file if exists
        if event.image:
            event.image.delete(save=False)

        # Save new file
        event.image = request.FILES["image"]
        event.save()

        serializer = self.get_serializer(event)
        return Response(serializer.data)
