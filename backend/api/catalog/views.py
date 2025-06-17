from rest_framework import viewsets
from rest_framework.permissions import (
    AllowAny,
)

from api.catalog.serializers import (
    ProductReadSerializer,
    ProductWriteSerializer
)
from catalog.models import Product


class ProductViewSet(viewsets.ModelViewSet):
    permission_classes = (AllowAny,)
    queryset = Product.objects.all()

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve', 'get-link'):
            return ProductReadSerializer
        return ProductWriteSerializer
