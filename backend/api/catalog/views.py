from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import (
    AllowAny,
)

from api.catalog.serializers import (
    ProductReadSerializer,
    ProductWriteSerializer
)
from api.permissions import IsDistributorReadOnly
from catalog.models import Product


class ProductViewSet(viewsets.ModelViewSet):
    permission_classes = (IsDistributorReadOnly,)
    queryset = Product.objects.all()
    pagination_class = PageNumberPagination
    filter_backends = (SearchFilter,)
    search_fields = ('^part_number',)

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve', 'get-link'):
            return ProductReadSerializer
        return ProductWriteSerializer
