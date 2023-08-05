from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # if is True, the whole thing return ture, will ignore "return obj.owner==request.user"
        if request.method in permissions.SAFE_METHODS:
            return True
        # return False or True
        return obj.owner == request.user
        # return super().has_object_permission(request, view, obj)