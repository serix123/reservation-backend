from rest_framework import viewsets
from reservation.models import Event
from reservation.serializers import EventSerializer


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    def get_queryset(self):
        queryset = self.queryset
        event_name = self.request.query_params.get("event_name")
        organizer_name = self.request.query_params.get("organizer_name")
        equipment_id = self.request.query_params.get("id")
        start_date = self.request.query_params.get("start_date")
        end_date = self.request.query_params.get("end_date")

        if start_date:
            queryset = queryset.filter(start_time__date=start_date)
        if end_date:
            queryset = queryset.filter(start_time__date=end_date)
        if start_date and end_date:
            queryset = queryset.filter(
                start_time__date__gte=start_date, end_time__date__lte=end_date
            )
        if event_name:
            queryset = queryset.filter(name__icontains=event_name)
        if organizer_name:
            queryset = queryset.filter(name__icontains=organizer_name)
        if equipment_id:
            queryset = queryset.filter(id=equipment_id)

        return queryset
