from rest_framework import serializers

from cart.cart import Cart
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

    class Meta:
        model = Order
        fields = (
            'id',
            'rs_code',
            'comment',
            )
        read_only_fields = ('product',)

    def create(self, validated_data):
        request = self.context.get('request')
        cart = Cart(request)
        rs_code = validated_data.pop('rs_code')
        comment = validated_data.pop('comment')
        order = Order.objects.create(
            rs_code=rs_code,
            comment=comment
        )
        for item in cart:
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                price=item['price_per_box'],
                count=item['count']
            )
        cart.clear()
        return order


class OrderReadSerializer(serializers.ModelSerializer):
    rs_code = serializers.ReadOnlyField(source='rs_code.rs_code')
    order_number = serializers.ReadOnlyField()
    products = OrderItemSerializer(many=True, source='items')

    class Meta:
        model = Order
        fields = (
            'id',
            'order_number',
            'rs_code',
            'products',
            'status',
            'created',
            'updated',
            'delivery_date',
            'comment',
            )
