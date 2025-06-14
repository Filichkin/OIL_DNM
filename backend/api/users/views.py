from djoser.views import UserViewSet
from rest_framework import viewsets

from api.users.permissions import (
    IsDistributor,
    IsDistributorOrIsAuthenticated
)
from api.users.serializers import (
    DealerCreateSerializer,
    DealerReadSerializer,
    SupplierCreateSerializer,
    SupplierReadSerializer,
    UserSerializer
)
from users.models import Dealer, Supplier, User


class UserViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsDistributor,)

    def get_permissions(self):
        if self.action == 'me':
            return (IsDistributorOrIsAuthenticated(),)
        return super().get_permissions()


class DealerViewSet(viewsets.ModelViewSet):
    queryset = Dealer.objects.all()
    permission_classes = (IsDistributor,)
    http_method_names = ('get', 'post', 'patch', 'delete')

    def get_serializer_class(self):
        if self.action in {'create', 'partial_update'}:
            return DealerCreateSerializer
        return DealerReadSerializer


class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    permission_classes = (IsDistributor,)
    http_method_names = ('get', 'post', 'patch', 'delete')

    def get_serializer_class(self):
        if self.action in {'create', 'partial_update'}:
            return SupplierCreateSerializer
        return SupplierReadSerializer
