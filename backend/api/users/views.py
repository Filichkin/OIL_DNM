from djoser.views import UserViewSet
from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination

from api.permissions import (
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
    pagination_class = PageNumberPagination
    filter_backends = (SearchFilter,)
    search_fields = ('^last_name',)

    def get_permissions(self):
        if self.action == 'me':
            return (IsDistributorOrIsAuthenticated(),)
        return super().get_permissions()


class DealerViewSet(viewsets.ModelViewSet):
    queryset = Dealer.objects.all().order_by('id')
    permission_classes = (IsDistributor,)
    pagination_class = PageNumberPagination
    filter_backends = (SearchFilter,)
    search_fields = ('^rs_code',)
    http_method_names = ('get', 'post', 'patch', 'delete')

    def get_serializer_class(self):
        if self.action in {'create', 'partial_update'}:
            return DealerCreateSerializer
        return DealerReadSerializer


class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all().order_by('id')
    permission_classes = (IsDistributor,)
    pagination_class = PageNumberPagination
    filter_backends = (SearchFilter,)
    search_fields = ('^name',)
    http_method_names = ('get', 'post', 'patch', 'delete')

    def get_serializer_class(self):
        if self.action in {'create', 'partial_update'}:
            return SupplierCreateSerializer
        return SupplierReadSerializer
