"""
This file contains the permissions for the chats app
"""

from rest_framework import permissions

class IsAuthenticated(permissions.BasePermission):
    """
    This class is used to check if the user is authenticated
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated