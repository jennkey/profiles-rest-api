from rest_framework import permissions


class UpdateOwnProfile(permissions.BasePermission):
    """ Allow users to edit their own profile. """

    def has_object_permission(self, request, view, obj):
        """ Check user is trying to edit their own profile. """

        # allow users list view - safe method
        if request.method in permissions.SAFE_METHODS:
            return True

        # Check if updating own profile
        return obj.id == request.user.id
