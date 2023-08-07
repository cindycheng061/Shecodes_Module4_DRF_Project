from rest_framework import permissions

class IsOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Allow admin to have permission
        if request.user.is_superuser:
            return True
        
        # Allow user to have permission if they own the profile
        return request.user == obj
