from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
import datetime

from reservation.models import Event, Notification
from reservation.serializers import EventSerializer


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]

    @staticmethod
    def round_to_nearest_quarter(dt):
        """Round a datetime to the nearest 15-minute mark."""
        new_minute = (dt.minute // 15 + (1 if dt.minute %
                      15 >= 7.5 else 0)) * 15
        return dt.replace(minute=0, second=0, microsecond=0) + datetime.timedelta(minutes=new_minute)

    def get_serializer_context(self):
        """Ensure that the request is added to the serializer context."""
        context = super(EventViewSet, self).get_serializer_context()
        context.update({
            "user": self.request.user
        })
        return context

    # def perform_create(self, serializer):
    #     user = self.request.user
    #     employee = Employee.objects.get(user=user)

    #     # This will save the Event instance
    #     instance = serializer.save(requesitioner=employee)

    #     # Automatically create an Approval instance when a new Event is created
    #     if instance.status == "application":
    #         Approval.objects.create(
    #             event=instance,
    #             # requesitioner=instance.requesitioner,
    #             requesitioner=employee,
    #             # Default status
    #             # status='pending'
    #         )

    # @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    # def cancel(self, request, pk=None):
    #     if pk is None:
    #         return Response({"error": "No event specified."}, status=status.HTTP_400_BAD_REQUEST)

    #     event = self.get_object()
    #     event.cancel_event()
    #     Notification.objects.create(
    #         recipient=event.requesitioner,  # Assuming requester has a user associated
    #         message=f"{event.event_name} has been cancelled",
    #         event=event
    #     )
    #     return Response({"status": "Event canceled"}, status=status.HTTP_200_OK)

    def get_queryset(self):
        queryset = self.queryset
        event_name = self.request.query_params.get("event_name")
        requesitioner = self.request.query_params.get("requesitioner")
        equipment_id = self.request.query_params.get("id")
        start_date = self.request.query_params.get("start_date")
        end_date = self.request.query_params.get("end_date")
        slip_number = self.request.query_params.get("slip_number")

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
        if requesitioner:
            queryset = queryset.filter(requesitioner=requesitioner)
        if slip_number:
            queryset = queryset.filter(slip_number=slip_number)
        if equipment_id:
            queryset = queryset.filter(id=equipment_id)

        return queryset
