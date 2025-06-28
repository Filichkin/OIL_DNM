from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from api.orders.serializers import (
    OrderCreateSerializer,
    OrderReadSerializer
)
from orders.models import Order


class OrderViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny,]
    queryset = Order.objects.all()

    def get_serializer_class(self):
        if self.action in {'create', 'partial_update'}:
            return OrderCreateSerializer
        return OrderReadSerializer
