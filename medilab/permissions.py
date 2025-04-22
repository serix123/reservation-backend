from rest_framework import permissions


class IsOwnerOrStaff(permissions.BasePermission):
    """
    Custom permission to only allow:
    - Staff users to perform any action
    - Owners to perform actions on their own profile
    - Read-only for others (though get_queryset restricts access further)
    """

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user or request.user.is_staff


class IsDoctor(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.is_staff
            and not request.user.is_superuser
        )


class IsPatientOwner(permissions.BasePermission):
    """Only allows patients to access their own profile"""

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsAdminOrReadOnly(permissions.BasePermission):
    """Allows read-only for non-admin, full access for admin"""

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_staff
