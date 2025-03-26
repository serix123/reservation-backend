from django.db import models
from authentication.models import User
from medilab.models import Patient


class MedicalRecord(models.Model):
    """
    Comprehensive medical record model to track patient visits and medical information.

    This model provides a structured way to document patient medical encounters,
    ensuring detailed and organized medical history tracking.
    """
    # Primary Key is automatically created by Django

    # Foreign Key to Patient model
    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name='medical_records',
        help_text="Patient associated with this medical record"
    )

    # Visit date and time
    visit_date = models.DateTimeField(
        auto_now_add=True,
        help_text="Date and time of the medical visit"
    )

    # Diagnosis field with choices and free text
    DIAGNOSIS_CATEGORIES = [
        ('GEN', 'General Checkup'),
        ('CHR', 'Chronic Condition'),
        ('ACS', 'Acute Syndrome'),
        ('INJ', 'Injury'),
        ('PRV', 'Preventive Care'),
        ('OTH', 'Other')
    ]

    diagnosis_category = models.CharField(
        max_length=3,
        choices=DIAGNOSIS_CATEGORIES,
        help_text="Broad category of the diagnosis"
    )

    diagnosis_details = models.TextField(
        help_text="Detailed description of the diagnosis",
        blank=True,
        null=True
    )

    # Treatment information
    treatment = models.TextField(
        help_text="Prescribed treatment or medical intervention",
        blank=True,
        null=True
    )

    # Attending Doctor (using User model for authentication)
    attending_doctor = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='medical_records_treated',
        help_text="Doctor who treated the patient"
    )

    # Additional notes
    notes = models.TextField(
        help_text="Additional medical notes or observations",
        blank=True,
        null=True
    )

    # Optional follow-up date
    follow_up_date = models.DateField(
        blank=True,
        null=True,
        help_text="Recommended date for follow-up appointment"
    )

    class Meta:
        verbose_name = 'Medical Record'
        verbose_name_plural = 'Medical Records'
        ordering = ['-visit_date']  # Most recent records first

        # Index for improved query performance
        indexes = [
            models.Index(fields=['patient', 'visit_date']),
            models.Index(fields=['attending_doctor', 'visit_date'])
        ]

    def __str__(self):
        """
        String representation of the medical record.
        Provides a quick summary for admin and debugging purposes.
        """
        return (
            f"Medical Record for {self.patient.get_full_name()} "
            f"on {self.visit_date.strftime('%Y-%m-%d')} - "
            f"{self.get_diagnosis_category_display()}"
        )

    def get_summary(self):
        """
        Generate a concise summary of the medical record.
        """
        return {
            'patient': self.patient.get_full_name(),
            'visit_date': self.visit_date,
            'diagnosis': self.diagnosis_details,
            'treatment': self.treatment,
            'doctor': self.attending_doctor.get_full_name() if self.attending_doctor else 'Unknown'
        }
