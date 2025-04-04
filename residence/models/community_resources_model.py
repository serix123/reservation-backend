# community/models.py
from django.db import models
from django.conf import settings


class CommunityResource(models.Model):
    RESOURCE_TYPES = [
        ('FOOD', 'Food Bank'),
        ('MED', 'Medical Supplies'),
        ('SHELTER', 'Emergency Shelter'),
        ('TOOL', 'Shared Tools'),
        ('EDU', 'Educational Resources'),
        ('OTHER', 'Other'),
    ]

    STATUS_CHOICES = [
        ('AVAILABLE', 'Available'),
        ('IN_USE', 'In Use'),
        ('MAINTENANCE', 'Under Maintenance'),
        ('UNAVAILABLE', 'Unavailable'),
    ]

    name = models.CharField(max_length=255)
    description = models.TextField()
    contact_info = models.CharField(max_length=255)
    resource_type = models.CharField(max_length=20, choices=RESOURCE_TYPES)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='AVAILABLE')
    managed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # Set in core.setting.py
        on_delete=models.SET_NULL,
        null=True,
        related_name='managed_resources'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.get_resource_type_display()})"

    class Meta:
        ordering = ['-created_at']
