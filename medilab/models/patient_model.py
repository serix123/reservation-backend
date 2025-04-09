from django.db import models
from django.conf import settings
from django.utils import timezone


class PatientProfile(models.Model):
    """The actual approved patient profile"""

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="patient_profile",
    )
    date_of_birth = models.DateField()
    address = models.TextField()
    village = models.CharField(max_length=100)
    medical_history = models.TextField(blank=True, null=True)
    approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="approved_profiles",
    )
    approval_date = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

    def create_update_application(self, changed_data=None):
        """
        Creates or updates the single allowed application per user.
        Overwrites any existing application and resets status to pending.
        """
        if changed_data is None:
            changed_data = {}

        # Get or create the single application for this user
        application, created = PatientProfileApplication.objects.get_or_create(
            user=self.user,
            defaults={
                "date_of_birth": changed_data.get("date_of_birth", self.date_of_birth),
                "address": changed_data.get("address", self.address),
                "village": changed_data.get("village", self.village),
                "medical_history": changed_data.get(
                    "medical_history", self.medical_history
                ),
                "id_proof_base64": changed_data.get("id_proof_base64", ""),
                "id_proof_filename": changed_data.get(
                    "id_proof_filename", "update_request"
                ),
                "status": "pending",
                "is_update": True if self.pk else False,
                "existing_profile": self if self.pk else None,
            },
        )

        # If application already existed, update it
        if not created:
            application.date_of_birth = changed_data.get(
                "date_of_birth", self.date_of_birth
            )
            application.address = changed_data.get("address", self.address)
            application.village = changed_data.get("village", self.village)
            application.medical_history = changed_data.get(
                "medical_history", self.medical_history
            )

            # Only update ID proof if new one is provided
            if "id_proof_base64" in changed_data:
                application.id_proof_base64 = changed_data["id_proof_base64"]
            if "id_proof_filename" in changed_data:
                application.id_proof_filename = changed_data["id_proof_filename"]

            application.status = "pending"  # Reset status
            application.save()

        return application

    class Meta:
        ordering = ["-created_at"]


class PatientProfileApplication(models.Model):
    """Application for patient profile that needs approval"""

    APPROVAL_STATUS = (
        ("pending", "Pending Approval"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile_applications",
    )
    date_of_birth = models.DateField()
    address = models.TextField()
    village = models.CharField(max_length=100)
    id_proof_base64 = models.TextField()  # Stores base64 encoded image
    id_proof_filename = models.CharField(max_length=255)  # Original filename
    medical_history = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=APPROVAL_STATUS, default="pending")
    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="reviewed_applications",
    )
    review_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # NEW FIELDS FOR UPDATE WORKFLOW:
    existing_profile = models.ForeignKey(
        PatientProfile,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="update_applications",
    )
    is_update = models.BooleanField(
        default=False
    )  # Tracks if this is an update request

    def __str__(self):
        return f"Application from {self.user.first_name} {self.user.last_name}"

    # UPDATED APPROVAL METHOD:
    def approve(self, approved_by):
        """Approve this application - now handles both new and update cases"""
        if self.is_update and self.existing_profile:
            # UPDATE CASE: Apply changes to existing profile
            profile = self.existing_profile
            profile.date_of_birth = self.date_of_birth
            profile.address = self.address
            profile.village = self.village
            profile.medical_history = self.medical_history
            profile.approved_by = approved_by
            profile.approval_date = timezone.now()
            profile.save()
        else:
            # NEW PROFILE CASE: Original creation logic
            PatientProfile.objects.create(
                user=self.user,
                date_of_birth=self.date_of_birth,
                address=self.address,
                village=self.village,
                medical_history=self.medical_history,
                approved_by=approved_by,
            )

        self.delete()  # Delete application after approval
        return True

        # Delete the application after successful profile creation
        self.delete()

        return True

    def reject(self, rejected_by):
        """Reject this application - we'll keep it for record-keeping"""
        self.status = "rejected"
        self.reviewed_by = rejected_by
        self.review_date = timezone.now()
        self.save()
        return True

    class Meta:
        ordering = ["-created_at"]
