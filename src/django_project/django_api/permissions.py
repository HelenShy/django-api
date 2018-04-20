from rest_framework import permissions


class UpdateOwnProfile(permissions.BasePermission):
    """
    Allow users to edit their profile.
    """
    def has_object_permission(self, request, view, obj):
        """
        Check user is trying to edit their own profile
        """
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.id == request.user.id


class PostOwnStatus(permissions.BasePermission):
    """
    Allow users to update their own status.
    """
    def has_object_permission(self, request, view, obj):
        """
        Check user is trying to update their own status
        """
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user_profile.id == request.user.id


class EditOwnLyrics(permissions.BasePermission):
    """
    Allow users to edit only lyrics posted by them.
    """
    def has_object_permission(self, request, view, obj):
        """
        Check user is trying to update lyrics posted by them
        """
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user_profile.id == request.user.id
