from django.db import models

from authentication.models import User


class Residence(models.Model):
    class Role(models.TextChoices):
        RESIDENT = 'Resident', 'Resident'
        ADMIN = 'Admin', 'Admin'
        OFFICER = 'Officer', 'Officer'
        # Add other roles as needed

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='residence'
    )
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    role = models.CharField(
        max_length=50,
        choices=Role.choices,
        default=Role.RESIDENT
    )
    contact_number = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    registration_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.role})"

    class Meta:
        db_table = "residence_info"  # Optional: Custom database table name


# class Residence(models.Model):
#     first_name = models.CharField(max_length=100, default="first_name")
#     last_name = models.CharField(max_length=100, default="last_name")
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     address = models.CharField(max_length=255)

#     REQUIRED_FIELDS = ["user"]

#     @property
#     def is_superuser(self):
#         return self.user.is_superuser

#     @property
#     def registration_date(self):
#         return self.user.date_joined

#     def save(self, *args, **kwargs):
#         # self.is_admin = self.user.is_superuser
#         super().save(*args, **kwargs)

#     def __str__(self):
#         return self.first_name + " " + self.last_name
