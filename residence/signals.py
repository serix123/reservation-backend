from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.utils import timezone
from residence.models import Residence
from authentication.models import User


@receiver(post_save, sender=User)
def create_residence_on_user_creation(sender, instance, created, **kwargs):
    """
    Automatically creates a Residence record when a new User is created
    """
    if created:
        Residence.objects.create(
            user=instance,
            first_name=instance.first_name,
            last_name=instance.last_name,
            contact_number="",  # Initialize empty
            address="",  # Initialize empty
        )


@receiver(post_save, sender=User)
def update_residence_role(sender, instance, **kwargs):
    # Update residence role when user permissions change
    if hasattr(instance, 'residence'):
        instance.residence.save()
