from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

# User = get_user_model()

# @receiver(post_save, sender=User)
# def create_patient_for_non_staff(sender, instance, created, **kwargs):
#     """
#     Optional: Automatically create a pending patient profile when a non-staff user registers.
#     If you prefer manual creation via API, you can skip this signal.
#     """
#     if created and not instance.is_staff:
#         Patient.objects.create(
#             user=instance,
#             date_of_birth="2000-01-01",  # Default values, should be updated via API
#             address="",
#             village="",
#             status="pending",
#         )
