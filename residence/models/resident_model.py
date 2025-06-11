from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Residence(models.Model):
    class Role(models.TextChoices):
        RESIDENT = "Resident", "Resident"
        GUARD = "Guard", "Guard"
        OFFICER = "Officer", "Officer"
        # Add other roles as needed

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="residence"
    )
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    role = models.CharField(max_length=50, choices=Role.choices, default=Role.RESIDENT)
    contact_number = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    registration_date = models.DateField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.first_name = self.user.first_name
        self.last_name = self.user.last_name
        # Automatically set role based on user's group
        user_groups = self.user.groups.values_list("name", flat=True)

        if "Resident" in user_groups:
            self.role = "Resident"
        elif "Guard" in user_groups:
            self.role = "Guard"
        elif "Officer" in user_groups:
            self.role = "Officer"
        else:
            self.role = "Resident"  # Default fallback
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.role})"

    class Meta:
        db_table = "residence_info"
