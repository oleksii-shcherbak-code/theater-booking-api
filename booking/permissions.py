from rest_framework.permissions import BasePermission


class IsOwnerOrAdmin(BasePermission):
    """
    Allow access only to booking owner or admin user.
    """

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user or request.user.is_staff
