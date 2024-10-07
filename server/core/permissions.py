# core/permissions.py

from rest_framework.permissions import BasePermission


class IsAdminOrReadOnly(BasePermission):
    """
    Custom permission to only allow admins to edit, but allow others to read.
    """

    def has_permission(self, request, view):
        if request.method in ("GET", "HEAD", "OPTIONS"):
            return True  # Safe methods for everyone
        return request.user.is_staff  # Only admins can make changes
