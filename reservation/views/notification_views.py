from django.db import transaction
from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from reservation.models import Employee, Notification
from reservation.serializers import NotificationSerializer


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_user_notification(request):
    # Try to get the employee or return 404 if not found
    user = request.user
    employee = Employee.objects.get(user=user)
    notification = Notification.objects.filter(recipient=employee).select_related('event')
    serializer = NotificationSerializer(notification, many=True)
    if serializer.is_valid:
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
