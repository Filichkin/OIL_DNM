from django.db.models import OuterRef, Subquery
from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination

from api.catalog.serializers import (
    CatalogCreateSerializer,
    CatalogReadSerializer,
    ProductReadSerializer,
    ProductCreateSerializer
)
from api.permissions import IsDistributorOrReadOnly
from catalog.models import Catalog, Product


class ProductViewSet(viewsets.ModelViewSet):
    permission_classes = (IsDistributorOrReadOnly,)
    queryset = Product.objects.all()
    pagination_class = PageNumberPagination
    filter_backends = (SearchFilter,)
    search_fields = ('^part_number',)
    http_method_names = ('get', 'post', 'patch', 'delete')

    def get_serializer_class(self):
        if self.action in {'create', 'partial_update'}:
            return ProductCreateSerializer
        return ProductReadSerializer


class CatalogViewSet(viewsets.ModelViewSet):
    permission_classes = (IsDistributorOrReadOnly,)
    queryset = Catalog.objects.annotate(
        supplier=Subquery(Product.objects.filter(
            part_number=OuterRef('part_number')).values('supplier__name')
            )
        )
    pagination_class = PageNumberPagination
    filter_backends = (SearchFilter,)
    search_fields = ('^part_number',)
    http_method_names = ('get', 'post', 'patch', 'delete')

    def get_serializer_class(self):
        if self.action in {'create', 'partial_update'}:
            return CatalogCreateSerializer
        return CatalogReadSerializer
