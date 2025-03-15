from django.db import models
from django.utils import timezone
from residence.models import Residence


class Issue(models.Model):
    class IssueStatus(models.TextChoices):
        OPEN = 'open', 'Open'
        RESOLVED = 'resolved', 'Resolved'

    title = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=IssueStatus.choices,
        default=IssueStatus.OPEN
    )
    resident = models.ForeignKey(
        Residence,
        on_delete=models.CASCADE,
        related_name='issues'
    )
    reported_date = models.DateTimeField(auto_now_add=True)
    resolved_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.title} - {self.get_status_display()}"

    class Meta:
        ordering = ['-reported_date']
