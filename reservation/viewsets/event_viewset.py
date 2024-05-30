import json
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.permissions import IsAuthenticated
import datetime

from reservation.models import Event, Notification, Employee
from reservation.serializers import EventSerializer


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    @staticmethod
    def round_to_nearest_quarter(dt):
        """Round a datetime to the nearest 15-minute mark."""
        new_minute = (dt.minute // 15 + (1 if dt.minute %
                      15 >= 7.5 else 0)) * 15
        return dt.replace(minute=0, second=0, microsecond=0) + datetime.timedelta(
            minutes=new_minute
        )

    def get_serializer_context(self):
        """Ensure that the request is added to the serializer context."""
        context = super(EventViewSet, self).get_serializer_context()
        context.update({"user": self.request.user})
        return context

    def create(self, request, *args, **kwargs):
        # Extract and parse the JSON data from the 'data' field in the multipart form
        data = request.data.get("data")
        if data:
            try:
                json_data = json.loads(
                    data
                )  # Convert JSON string back to Python dictionary
            except json.JSONDecodeError:
                return Response(
                    {"error": "Invalid JSON data"}, status=status.HTTP_400_BAD_REQUEST
                )
        else:
            return Response(
                {"error": "No data provided"}, status=status.HTTP_400_BAD_REQUEST
            )

        # Handle file if included
        if "event_file" in request.FILES:
            json_data["event_file"] = request.FILES["event_file"]

        serializer = self.get_serializer(data=json_data)
        if serializer.is_valid():
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(
                serializer.data, status=status.HTTP_201_CREATED, headers=headers
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def update(self, request, *args, **kwargs):
        # data = request.data.get("data")
        # instance = self.get_object()
        # if data:
        #     try:
        #         json_data = json.loads(
        #             data
        #         )  # Convert JSON string back to Python dictionary
        #     except json.JSONDecodeError:
        #         return Response(
        #             {"error": "Invalid JSON data"}, status=status.HTTP_400_BAD_REQUEST
        #         )
        # else:
        #     return Response(
        #         {"error": "No data provided"}, status=status.HTTP_400_BAD_REQUEST
        #     )

        # # Handle file if included
        # if "event_file" in request.FILES:
        #     json_data["event_file"] = request.FILES["event_file"]

        # serializer = self.get_serializer(
        #     instance, data=json_data, partial=True)
        # if serializer.is_valid():
        #     self.perform_update(serializer)
        #     headers = self.get_success_headers(serializer.data)
        #     return Response(
        #         serializer.data, status=status.HTTP_200_OK
        #     )
        # else:
        #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        queryset = Event.objects.all()
        #     event_name = self.request.query_params.get("event_name")
        #     requesitioner = self.request.query_params.get("requesitioner")
        #     equipment_id = self.request.query_params.get("id")
        #     start_date = self.request.query_params.get("start_date")
        #     end_date = self.request.query_params.get("end_date")
        slip_number = self.request.query_params.get("slip_number")
        #     # user_only = self.request.query_params.get("user_only")

        #     # if user_only == True:
        #     #     user = self.request.user
        #     #     employee = Employee.objects.get(user=user)
        #     #     queryset = queryset.filter(requesitioner=employee)

        #     if start_date:
        #         queryset = queryset.filter(start_time__date=start_date)
        #     if end_date:
        #         queryset = queryset.filter(start_time__date=end_date)
        #     if start_date and end_date:
        #         queryset = queryset.filter(
        #             start_time__date__gte=start_date, end_time__date__lte=end_date
        #         )
        #     if event_name:
        #         queryset = queryset.filter(name__icontains=event_name)
        #     if requesitioner:
        #         queryset = queryset.filter(requesitioner=requesitioner)
        if slip_number:
            queryset = queryset.filter(slip_number=slip_number)
        #     if equipment_id:
        #         queryset = queryset.filter(id=equipment_id)

        return queryset
