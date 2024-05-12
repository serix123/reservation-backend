import json
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser

from reservation.models import Employee, Event, Notification
from reservation.serializers import EventSerializer


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def cancel_event(request, slip_number):
    if slip_number is None:
        return Response(
            {"error": "No event specified."}, status=status.HTTP_400_BAD_REQUEST
        )

    event = Event.objects.get(slip_number=slip_number)
    if event.status in ("application", "confirmed", "returned"):
        event.cancel_event()
        Notification.objects.create(
            recipient=event.requesitioner,  # Assuming requester has a user associated
            message=f"{event.event_name} has been cancelled",
            event=event,
        )
        return Response({"status": "Event cancelled"}, status=status.HTTP_200_OK)
    else:
        return Response(
            {"error": "No event specified."}, status=status.HTTP_400_BAD_REQUEST
        )


@api_view(["GET"])
def user_event(request):
    """
    Fully update an event identified by slip_number.
    """
    user = request.user
    employee = Employee.objects.get(user=user)
    event = Event.objects.filter(requesitioner=employee)
    serializer = EventSerializer(event, many=True)
    return Response(serializer.data)


@api_view(["PUT"])
def update_event(request, slip_number):
    """
    Fully update an event identified by slip_number.
    """
    event = get_object_or_404(Event, slip_number=slip_number)
    serializer = EventSerializer(
        event, data=request.data, context={"user": request.user}
    )
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["PATCH"])
@parser_classes([MultiPartParser, FormParser])
def partial_update_event(request, slip_number):
    """
    Partially update an event identified by slip_number.
    """

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

    event = get_object_or_404(Event, slip_number=slip_number)
    serializer = EventSerializer(
        # event, data=request.data, partial=True, context={"user": request.user}
        event,
        data=json_data,
        partial=True,
        context={"user": request.user},
    )
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
