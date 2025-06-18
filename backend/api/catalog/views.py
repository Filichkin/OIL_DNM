from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination

from api.catalog.serializers import (
    ProductReadSerializer,
    ProductCreateSerializer
)
from api.permissions import IsDistributorOrReadOnly
from catalog.models import Product


class ProductViewSet(viewsets.ModelViewSet):
    permission_classes = (IsDistributorOrReadOnly,)
    queryset = Product.objects.all()
    pagination_class = PageNumberPagination
    filter_backends = (SearchFilter,)
    search_fields = ('^part_number',)
    http_method_names = ('GET', 'POST', 'PATCH', 'DELETE')

    def get_serializer_class(self):
        if self.action in {'create', 'partial_update'}:
            return ProductCreateSerializer
        return ProductReadSerializer
