from rest_framework import permissions


class IsDistributor(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_distributor

    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and request.user.is_distributor


class IsDistributorOrIsAuthenticated(permissions.IsAuthenticated):

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            or request.user.is_distributor
        )


class IsDistributorOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return (
            (
                request.method in permissions.SAFE_METHODS
                and request.user.is_authenticated
                )
            or (request.user.is_authenticated and request.user.is_distributor)
        )


class IsDistributorOrDealer(permissions.BasePermission):

    def has_permission(self, request, view):
        return (
            (request.user.is_authenticated and request.user.is_distributor)
            or (request.user.is_authenticated and request.user.is_dealer)
        )


class IsDistributorOrDealerOrSupplier(permissions.BasePermission):

    def has_permission(self, request, view):
        return (
            (request.user.is_authenticated and request.user.is_distributor)
            or (request.user.is_authenticated and request.user.is_dealer)
            or (request.user.is_authenticated and request.user.is_supplier)
        )
