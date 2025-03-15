from rest_framework import permissions


class IsResidentOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.host_residence.user == request.user


class IsAdminOrOfficer(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return (
            user.is_authenticated and
            (
                user.is_staff or
                getattr(user.residence, 'role', None) in ['Admin', 'Officer']
            )
        )
