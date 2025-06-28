from rest_framework import serializers

from orders.models import Order, OrderItem
from users.models import Dealer


class OrderCreateSerializer(serializers.ModelSerializer):
    rs_code = serializers.PrimaryKeyRelatedField(
        queryset=Dealer.objects.all(),
        label='Dealer'
    )
    comment = serializers.CharField(required=False)

    class Meta:
        model = Order
        fields = (
            'id',
            'rs_code',
            'comment',
            )


class OrderReadSerializer(serializers.ModelSerializer):
    rs_code = serializers.ReadOnlyField(source='rs_code.rs_code')
    order_number = serializers.ReadOnlyField()

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


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = (
            'id',
            'order',
            'product',
            'count',
            'created_at',
            'updated_at'
            )
        read_only_fields = ('id', 'created_at', 'updated_at')
