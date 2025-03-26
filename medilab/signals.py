from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from medilab.models import Patient


@receiver(post_save, sender=User)
def create_patient_profile(sender, instance, created, **kwargs):
    """
    Signal receiver to automatically create a patient profile 
    when a new user is registered.
    
    Note: This requires minimal patient information. 
    Users/admins should update details later.
    """
    if created:
        # Create a basic patient profile with minimal information
        Patient.objects.create(
            user=instance,
            first_name=instance.first_name or instance.username,
            last_name=instance.last_name or '',
            birthdate='1990-01-01',  # Default placeholder
            gender='N'  # Prefer not to say
        )

# Optional: Ensure signal is imported when Django loads the app


def ready(self):
    import patients.signals
