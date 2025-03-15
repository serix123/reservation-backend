from django.conf import settings
from django.db import models
from django.utils import timezone
from authentication.models import User


class Event(models.Model):
    name = models.CharField(max_length=200)
    date = models.DateTimeField(default=timezone.now)
    details = models.TextField()
    location = models.CharField(max_length=255)
    creator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='created_events'
    )
    attendees = models.ManyToManyField(
        User,
        related_name='attended_events',
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.date.strftime('%Y-%m-%d')}"

    @property
    def attendees_count(self):
        return self.attendees.count()

    class Meta:
        ordering = ['-date']
