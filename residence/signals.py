from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.utils import timezone
from residence.models import Residence


User = get_user_model()


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

GROUP_ROLE_MAP = {
    "Resident": "Resident",
    "Officer": "Officer",
    "Guard": "Guard",
}

ROLE_GROUP_MAP = {v: k for k, v in GROUP_ROLE_MAP.items()}

# @receiver(m2m_changed, sender=Group.user_set.through)
# def sync_residence_role_on_group_change(sender, instance, action, **kwargs):
#     if action in ["post_add", "post_remove", "post_clear"]:
#         try:
#             residence = instance.residence
#             user_groups = instance.groups.values_list("name", flat=True)
#             for group in user_groups:
#                 if group in GROUP_ROLE_MAP:
#                     residence.role = GROUP_ROLE_MAP[group]
#                     residence.save()
#                     break
#         except Residence.DoesNotExist:
#             pass


@receiver(post_save, sender=Residence)
def sync_user_group_on_role_change(sender, instance, **kwargs):
    user = instance.user
    role = instance.role

    if role in ROLE_GROUP_MAP:
        # Clear previous related groups
        user.groups.clear()

        # Add the correct group
        try:
            group = Group.objects.get(name=ROLE_GROUP_MAP[role])
            user.groups.add(group)
        except Group.DoesNotExist:
            pass
