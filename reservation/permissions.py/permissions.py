from rest_framework import permissions


class IsOrganizerSuperior(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # obj refers to the Approval instance
        return obj.applicant.immediate_head == request.user
