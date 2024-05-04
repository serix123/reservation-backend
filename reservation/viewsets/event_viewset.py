from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from reservation.models import Event
from reservation.serializers import EventSerializer


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        """Ensure that the request is added to the serializer context."""
        context = super(EventViewSet, self).get_serializer_context()
        context.update({
            "request": self.request
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

    def get_queryset(self):
        queryset = self.queryset
        event_name = self.request.query_params.get("event_name")
        requesitioner = self.request.query_params.get("requesitioner")
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
        if requesitioner:
            queryset = queryset.filter(requesitioner=requesitioner)
        if equipment_id:
            queryset = queryset.filter(id=equipment_id)

        return queryset
