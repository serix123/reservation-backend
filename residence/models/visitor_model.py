from django.db import models
from django.utils import timezone
from residence.models import Residence


class Visitor(models.Model):
    class VisitStatus(models.TextChoices):
        PENDING = 'pending', 'Pending'
        CHECKED_IN = 'checked_in', 'Checked In'
        CHECKED_OUT = 'checked_out', 'Checked Out'

    residence = models.ForeignKey(  # Keep lowercase and fix schema
        Residence,
        on_delete=models.CASCADE,
        related_name='visitors'
    )
    name = models.CharField(max_length=255)
    visit_date = models.DateTimeField(default=timezone.now)
    visit_purpose = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=VisitStatus.choices,
        default=VisitStatus.PENDING
    )
    check_in_time = models.DateTimeField(null=True, blank=True)
    check_out_time = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.get_status_display()}"

    class Meta:
        ordering = ['-visit_date']
