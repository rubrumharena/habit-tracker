from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    def has_permission(self, request, view):
        if request.user.username == view.kwargs.get('username'):
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.user.username == obj.user.username:
            return True
        return False