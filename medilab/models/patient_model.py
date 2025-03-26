from django.db import models
from authentication.models import User
from django.core.validators import EmailValidator, RegexValidator


class Patient(models.Model):
    """
    Model representing a patient in the medical management system.

    This model captures essential patient demographic information 
    and uses Django's built-in User model for authentication and 
    user-related details.
    """
    # Primary Key is automatically created by Django as 'id'

    # Foreign Key to Django's User model for authentication and user details
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,  # If user is deleted, patient record is also deleted
        related_name='patients',   # Allows reverse lookup from User to Patient
        null=True,                 # Allow patients without a user account
        blank=True                 # Make the field optional in forms
    )

    # Patient's personal information
    first_name = models.CharField(
        max_length=100,
        help_text="Patient's first name"
    )

    last_name = models.CharField(
        max_length=100,
        help_text="Patient's last name"
    )

    # Using DateField for birthdate to store the exact date of birth
    birthdate = models.DateField(
        help_text="Patient's date of birth"
    )

    # Predefined choices for gender to ensure data consistency
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
        ('N', 'Prefer Not to Say')
    ]

    gender = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES,
        default='N',
        help_text="Patient's gender"
    )

    # Comprehensive address field
    address = models.TextField(
        help_text="Patient's full address",
        blank=True,  # Optional address field
        null=True
    )

    # Email field with validation
    email = models.EmailField(
        unique=True,
        validators=[EmailValidator()],
        help_text="Patient's primary email address",
        blank=True,
        null=True
    )

    # Optional phone number with validation
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )
    phone_number = models.CharField(
        validators=[phone_regex],
        max_length=17,
        blank=True,
        null=True,
        help_text="Patient's primary contact number"
    )

    # Metadata and utility methods
    class Meta:
        verbose_name = 'Patient'
        verbose_name_plural = 'Patients'
        # Optional: Add index on frequently searched fields
        indexes = [
            models.Index(fields=['last_name', 'first_name']),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=['email'],
                name='unique_patient_email',
                condition=models.Q(email__isnull=False)
            )
        ]

    def __str__(self):
        """
        String representation of the Patient model.
        Useful for admin interface and debugging.
        """
        return f"{self.first_name} {self.last_name}"

    def get_full_name(self):
        """
        Convenience method to get the patient's full name.
        """
        return f"{self.first_name} {self.last_name}"
