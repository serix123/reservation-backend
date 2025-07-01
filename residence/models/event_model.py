from django.conf import settings
from django.db import models
from django.utils import timezone
from datetime import timedelta
from authentication.models import User
from residence.models import Residence


class Event(models.Model):

    class EventStatus(models.TextChoices):
        TENTATIVE = "tentative", "Tentative"
        CONFIRMED = "confirmed", "Confirmed"
        REJECTED = "rejected", "Rejected"

    name = models.CharField(max_length=200)
    date = models.DateTimeField(default=timezone.now)
    duration = models.DurationField(default=timedelta(hours=1))
    # status = models.CharField(
    #     max_length=20, choices=EventStatus.choices, default=EventStatus.TENTATIVE
    # )
    details = models.TextField()

    class LocationChoices(models.TextChoices):
        BLOCK_1 = "Block 1", "Block 1"
        BLOCK_2A = "Block 2A", "Block 2A"
        BLOCK_2A1 = "Block 2A1", "Block 2A1"
        BLOCK_2B = "Block 2B", "Block 2B"
        BLOCK_2C = "Block 2C", "Block 2C"
        BLOCK_3 = "Block 3", "Block 3"
        BLOCK_4 = "Block 4", "Block 4"
        BLOCK_5 = "Block 5", "Block 5"
        BLOCK_6A = "Block 6A", "Block 6A"
        BLOCK_6B = "Block 6B", "Block 6B"
        BLOCK_7 = "Block 7", "Block 7"
        BLOCK_8 = "Block 8", "Block 8"
        BLOCK_9 = "Block 9", "Block 9"
        BLOCK_10 = "Block 10", "Block 10"
        BLOCK_11 = "Block 11", "Block 11"
        BLOCK_12 = "Block 12", "Block 12"

    location = models.CharField(
        max_length=20,
        choices=LocationChoices.choices,
        default=LocationChoices.BLOCK_1,
        help_text="Select the block where the event will take place.",
    )
    creator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="created_events",
    )
    attendees = models.ManyToManyField(
        Residence, related_name="attended_events", blank=True
    )
    image = models.ImageField(upload_to="event_images/", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.date.strftime('%Y-%m-%d')}"

    @property
    def attendees_count(self):
        return self.attendees.count()

    @property
    def end_time(self):
        """
        Returns the computed end time: date + duration.
        Returns None if duration is not set.
        """
        if self.duration:
            return self.date + self.duration
        return None

    # class Meta:
    #     ordering = ["-updated_at", "created_at"]
