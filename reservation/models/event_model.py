from django.db import models
from reservation.models import Facility, Employee


class Event(models.Model):
    event_name = models.CharField(max_length=255)
    event_description = models.TextField(blank=True, null=True)
    organizer_name = models.ForeignKey(
        "Employee", on_delete=models.CASCADE, related_name="events"
    )
    reserved_facility = models.ForeignKey(
        "Facility", on_delete=models.CASCADE, related_name="events"
    )
    department = models.ForeignKey(
        "Department",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="events",
    )
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    equipment = models.ManyToManyField("Equipment", blank=True, related_name="events")
    STATUS_TYPE = (
        (1, "Pending"),
        (2, "Confirmed"),
        (3, "Cancelled"),
        (4, "Denied"),
        (5, "Draft"),
    )
    status = models.IntegerField(default=5, choices=STATUS_TYPE)

    is_recurring = models.BooleanField(default=False)
    days_of_week = models.CharField(
        max_length=15, blank=True, null=True
    )  # CSV like "1,3,5" for Mon, Wed, Fri

    def get_weekday_display(self):
        weekdays = {
            "1": "Monday",
            "2": "Tuesday",
            "3": "Wednesday",
            "4": "Thursday",
            "5": "Friday",
            "6": "Saturday",
            "7": "Sunday",
        }
        days = (weekdays.get(day, "") for day in self.days_of_week.split(","))
        return ", ".join(filter(None, days))

    def __str__(self):
        return f"{self.facility.name} reservation by {str(self.employee)} on {self.start_time.strftime('%Y-%m-%d %H:%M')}"

    class Meta:
        ordering = ["event_name"]
