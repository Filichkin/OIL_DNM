from django.db.models import OuterRef, Subquery
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from api.catalog.serializers import (
    OrderCreateSerializer,
    CatalogCreateSerializer,
    CatalogReadSerializer,
    ProductReadSerializer,
    ProductCreateSerializer
)
from api.permissions import IsDistributorOrReadOnly
from cart.models import OrderList
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
        elif self.action == 'cart':
            return OrderCreateSerializer
        return CatalogReadSerializer

    @staticmethod
    def add_to(serializer_class, request, id):
        serializer = serializer_class(
            data={
                'dealer': request.data.get('dealer', 1),
                'product': id,
                'count': request.data.get('count', 1),
                },
            context={'request': request},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @staticmethod
    def delete_from(model, request, id):
        obj = model.objects.filter(dealer=request.dealer, product__id=id)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=True,
        methods=['POST', 'DELETE'],
        permission_classes=[AllowAny],
        url_path='cart',
        url_name='cart',
    )
    def cart(self, request, pk=None):
        if request.method == 'POST':
            return self.add_to(OrderCreateSerializer, request, pk)
        return self.delete_from(OrderList, request, pk)
