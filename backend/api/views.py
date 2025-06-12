from djoser.views import UserViewSet
from rest_framework import viewsets

from api.permissions import IsDistributor, IsDistributorOrIsAuthenticated
from api.serializers import (
    DealerAddSerializer,
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


class DealerViewSer(viewsets.ModelViewSet):
    queryset = Dealer.objects.all()
    permission_classes = (IsDistributorOrIsAuthenticated,)

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve', 'get-link'):
            return DealerReadSerializer
        return DealerAddSerializer
