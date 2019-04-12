from rest_framework import permissions


class SuperUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_superuser


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_staff


class IsSuperOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_staff:
            if request.method in permissions.SAFE_METHODS:
                return True
            return request.user.is_superuser
        else:
            return False

