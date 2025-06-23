from rest_framework import permissions
from django.contrib.auth.models import Group


class IsResidentOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.host_residence.user == request.user


class IsAdminOrOfficer(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return user.is_authenticated and (
            user.is_staff
            or getattr(user.residence, "role", None) in ["Admin", "Officer"]
        )


class SecurityStaffPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.is_staff
            and not request.user.is_superuser
        )


class IsOfficer(permissions.BasePermission):
    """
    Custom permission to only allow users in the 'Officer' group.
    """

    message = "You must be an Officer to perform this action."

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.groups.filter(name="Officer").exists()
        )

    def has_object_permission(self, request, view, obj):
        # Guards might have full object permissions or limited, matching Officer for now
        return self.has_permission(request, view)


class IsResident(permissions.BasePermission):
    """
    Custom permission to only allow users in the 'Resident' group.
    """

    message = "You must be a Resident to perform this action."

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.groups.filter(name="Resident").exists()
        )

    def has_object_permission(self, request, view, obj):
        # Check if the object has a `user` or `creator` attribute
        owner = getattr(obj, "user", None) or getattr(obj, "creator", None)

        if owner is None:
            return False  # If neither exists, deny access

        return owner == request.user and self.has_permission(request, view)


class IsGuard(permissions.BasePermission):
    """
    Custom permission to only allow users in the 'Guard' group.
    (Less likely needed for specific write actions, often just for read views)
    """

    message = "You must be a Guard to perform this action."

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.groups.filter(name="Guard").exists()
        )

    def has_object_permission(self, request, view, obj):
        # Guards might have full object permissions or limited, matching Officer for now
        return self.has_permission(request, view)


class IsOwner(permissions.BasePermission):
    """
    Custom permission to allow object access only to the owner (reporter) of the issue.
    """

    def has_object_permission(self, request, view, obj):
        # Object-level permission check
        return obj.user == request.user


# A combined permission for roles that can read all events (Officer, Superuser, Creator)
class CanViewAll(permissions.BasePermission):
    """
    Custom permission to determine if a user can view all event statuses.
    Used internally by get_queryset.
    """

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False  # Unauthenticated users only see CONFIRMED via get_queryset

        # Superusers and Officers can view all events
        return (
            request.user.is_superuser
            or request.user.groups.filter(name="Officer").exists()
        )
