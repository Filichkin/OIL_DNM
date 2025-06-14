from djoser.views import UserViewSet
from rest_framework import viewsets

from api.permissions import IsDistributor, IsDistributorOrIsAuthenticated
from api.serializers import (
    DealerCreateSerializer,
    DealerReadSerializer,
    UserSerializer
)
from users.models import Dealer, User


class UserViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsDistributor,)

    def get_permissions(self):
        if self.action == 'me':
            return (IsDistributorOrIsAuthenticated(),)
        return super().get_permissions()


class DealerViewSet(viewsets.ModelViewSet):
    queryset = Dealer.objects.annotate()
    permission_classes = (IsDistributorOrIsAuthenticated,)
    http_method_names = ('get', 'post', 'patch', 'delete')

    def get_serializer_class(self):
        if self.action in {'create', 'partial_update'}:
            return DealerCreateSerializer
        return DealerReadSerializer
