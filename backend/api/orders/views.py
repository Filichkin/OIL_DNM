from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response
# from rest_framework.permissions import AllowAny

from api.orders.serializers import (
    OrderCreateSerializer,
    OrderReadSerializer,
    OrderUpdateSerializer,
)
from api.permissions import IsDistributorOrDealerOrSupplier
from orders.models import Order


class OrderViewSet(viewsets.ModelViewSet):
    permission_classes = [IsDistributorOrDealerOrSupplier,]
    queryset = Order.objects.all()
    http_method_names = ('get', 'post', 'patch', 'delete')

    def get_serializer_class(self):
        if self.action == 'create':
            return OrderCreateSerializer
        if self.action == 'partial_update':
            return OrderUpdateSerializer
        return OrderReadSerializer

    # def patch(self, request, order_id):
    #     order = get_object_or_404(Order, pk=order_id)
    #     serializer = OrderUpdateSerializer(
    #         order,
    #         data=request.data,
    #     )
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     return Response(serializer.data)
