from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from medilab.models import Patient

User = get_user_model()


@receiver(post_save, sender=User)
def create_patient_profile(sender, instance, created, **kwargs):
    """
    Automatically create a Patient profile when a new regular user is created.
    """
    if created and not instance.is_staff and not instance.is_superuser:
        Patient.objects.create(
            user=instance,
            first_name=instance.first_name,
            last_name=instance.last_name,
            # Other fields will be filled during verification
            verification_status="unverified",
        )


@receiver(post_save, sender=Patient)
def update_user_profile(sender, instance, **kwargs):
    """
    Updates the related User instance whenever a Patient instance is saved.
    """
    try:
        user = instance.user
        if user:
            # user.email = instance.email
            user.first_name = instance.first_name
            user.last_name = instance.last_name
            user.save()
    except User.DoesNotExist:
        # Handle the case where the related User might not exist (though with OneToOne, this is unlikely after creation)
        pass
