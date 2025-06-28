from rest_framework import serializers

from catalog.models import Catalog
from orders.models import Order, OrderItem
from users.models import Dealer


class OrderItemSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(
        queryset=Catalog.objects.all(),
        label='Product'
    )

    class Meta:
        fields = (
            'id',
            'order',
            'product',
            'price',
            'count'
            )
        model = OrderItem


class OrderCreateSerializer(serializers.ModelSerializer):
    rs_code = serializers.PrimaryKeyRelatedField(
        queryset=Dealer.objects.all(),
        label='Dealer'
    )
    comment = serializers.CharField(required=False)
    products = OrderItemSerializer(many=True, required=True)

    class Meta:
        model = Order
        fields = (
            'id',
            'rs_code',
            'comment',
            'products'
            )


class OrderReadSerializer(serializers.ModelSerializer):
    rs_code = serializers.ReadOnlyField(source='rs_code.rs_code')
    order_number = serializers.ReadOnlyField()
    products = OrderItemSerializer(many=True, source='items')

    class Meta:
        model = Order
        fields = (
            'id',
            'order_number'
            'rs_code',
            'status',
            'created',
            'updated',
            'delivery_date',
            'comment',
            )
