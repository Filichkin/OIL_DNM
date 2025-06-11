from rest_framework import permissions


class IsDistributor(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_distributor


class IsDistributorOrIsAuthenticated(permissions.IsAuthenticated):

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            or request.user.is_distributor
        )
