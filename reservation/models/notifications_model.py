from django.db import models
from django.conf import settings

from reservation.models.employee_model import Employee
from reservation.models.event_model import Event


class Notification(models.Model):
    recipient = models.ForeignKey(
        Employee, on_delete=models.CASCADE, related_name='notifications')
    message = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    event = models.ForeignKey(Event, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f'Notification for {self.recipient} about {self.event}'
