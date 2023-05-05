from rest_framework import permissions

class IsAdminUserOrSelf(permissions.BasePermission):
    """
    Object-level permission to allow only admin users or the object owner to edit or delete it.
    """

    def has_object_permission(self, request, view, obj):
        # Check if the user is an admin or the object owner
        return request.user.is_staff or obj == request.user
