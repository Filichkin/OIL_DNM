from djoser.views import UserViewSet
from rest_framework.permissions import IsAuthenticated

from api.serializers import UserSerializer
from users.models import User


class UserViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == 'me':
            return (IsAuthenticated(),)
        return super().get_permissions()
