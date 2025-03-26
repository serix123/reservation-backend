from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly
from rest_framework.decorators import action
from rest_framework.response import Response
from residence.models import Event
from residence.serializers import EventSerializer, CreateEventSerializer, AttendEventSerializer


class EventViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    filterset_fields = ['creator', 'date']
    ordering_fields = ['date', 'attendees_count']
    search_fields = ['name', 'location', 'details']

    def get_serializer_class(self):
        if self.action == 'create':
            return CreateEventSerializer
        if self.action == 'attend':
            return AttendEventSerializer
        return EventSerializer

    def get_queryset(self):
        return Event.objects.prefetch_related('attendees').all()

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    @action(detail=True, methods=['post'])
    def attend(self, request, pk=None):
        event = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        action = serializer.validated_data['action']
        user = request.user

        if action == 'attend':
            event.attendees.add(user)
        elif action == 'unattend':
            event.attendees.remove(user)

        return Response(  # Fixed parentheses here
            EventSerializer(event, context={'request': request}).data,
            status=status.HTTP_200_OK
        )

    @action(detail=False, methods=['get'])
    def upcoming(self, request):
        queryset = self.filter_queryset(
            self.get_queryset().filter(date__gte=timezone.now())
        )
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)
