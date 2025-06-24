from django.db.models import OuterRef, Subquery
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from api.catalog.serializers import (
    CartContentSerializer,
    CartItemSerializer,
    CartItemDeleteSerializer,
    CatalogCreateSerializer,
    CatalogReadSerializer,
    ProductReadSerializer,
    ProductCreateSerializer,
)
from api.permissions import (
    IsDistributorOrDealer,
    IsDistributorOrReadOnly
)
from cart.cart import Cart
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
            return CartItemSerializer
        return CatalogReadSerializer

    @staticmethod
    def add_to_cart(product, request):
        serializer = CartItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        cart = Cart(request)
        try:
            cart.add(
                product=product,
                count=serializer.validated_data['count'],
                dealer=serializer.validated_data['dealer'],
            )
            return Response(
                {
                    'message': 'Item added to cart'
                    },
                status=status.HTTP_201_CREATED
            )
        except NotFound:
            return Response(
                {'product_id': 'Product ID not found'},
                status=status.HTTP_404_NOT_FOUND,
            )

    @action(
        detail=True,
        methods=['POST'],
        permission_classes=[IsDistributorOrDealer],
        url_path='cart',
        url_name='cart',
    )
    def cart(self, request, pk):
        product = get_object_or_404(Catalog, pk=pk)
        if request.user.is_dealer:
            request.data['dealer'] = request.user.rs_code.id
            return self.add_to_cart(product, request)
        return self.add_to_cart(product, request)


class CartView(APIView):
    permission_classes = (IsDistributorOrDealer,)
    serializer_class = CartContentSerializer

    def post(self, request, *args, **kwargs):
        cart = Cart(request)
        cart.clear()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get(self, request, *args, **kwargs):

        query_params = request.query_params

        # Validate allowed parameters
        allowed_params = {'count', 'items', 'total_price'}
        invalid_params = set(query_params.keys()) - allowed_params
        if invalid_params:
            raise ValidationError(
                {
                    'error': f"Invalid query parameters: "
                             f"{', '.join(invalid_params)}"
                    }
            )
        get_total_count = 'count' in query_params
        get_total_items = 'items' in query_params
        get_total_price = 'total_price' in query_params

        cart = Cart(request)

        if get_total_count:
            return Response({'total_count': len(cart)}, status=206)

        cart_items = cart.get_cart_items()

        if get_total_items:
            return Response({'cart_items': len(cart_items)}, status=206)

        if get_total_price:
            return Response({'total_price': cart.get_total_price}, status=201)

        serializer = CartContentSerializer(cart, many=True)
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        serializer = CartItemDeleteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        cart = Cart(request)
        try:
            cart.remove(
                product_id=serializer.validated_data['product_id'],
                dealer=serializer.validated_data['dealer'],
            )
            return Response(
                {
                    'message': 'Item deleted from cart'
                    },
                status=status.HTTP_204_NO_CONTENT
            )
        except NotFound:
            return Response(
                {'product_id': 'Product ID not found'},
                status=status.HTTP_404_NOT_FOUND,
            )
