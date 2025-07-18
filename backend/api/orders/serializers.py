from django.shortcuts import get_object_or_404
from rest_framework import serializers

from api.orders.utils import generate_order_number
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
        label='Dealer',
        required=False
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

    @staticmethod
    def create_order_item(order, item):
        return OrderItem.objects.create(
            order=order,
            product=item['product'],
            price=item['price_per_box'],
            count=item['count']
            )

    def create(self, validated_data):
        request = self.context.get('request')
        if request.user.is_dealer:
            rs_code = request.user.rs_code.id
            dealer = get_object_or_404(Dealer, pk=rs_code)
        else:
            dealer = validated_data.pop('rs_code')
        cart = Cart(request)
        comment = validated_data.pop('comment')
        order_automarket = Order.objects.create(
            dealer=dealer,
            comment=comment
        )
        order_lemarc = Order.objects.create(
            dealer=dealer,
            comment=comment
        )
        order_number_automarket = None
        order_number_lemarc = None
        for item in cart:
            if item['brand'] == 'S-Oil':
                order_number_automarket = generate_order_number(dealer, 'A')
                order_automarket.order_number = order_number_automarket
                order_automarket.save()
                self.create_order_item(order_automarket, item)
            if item['brand'] == 'Lemarc':
                order_number_lemarc = generate_order_number(dealer, 'L')
                order_lemarc.order_number = order_number_lemarc
                order_lemarc.save()
                self.create_order_item(order_lemarc, item)
        cart.clear()
        if order_number_lemarc is None:
            order_lemarc.delete()
            return order_automarket
        elif order_number_automarket is None:
            order_automarket.delete()
            return order_lemarc
        return order_automarket, order_lemarc


class OrderReadSerializer(serializers.ModelSerializer):
    rs_code = serializers.ReadOnlyField(source='dealer.rs_code')
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


class OrderUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('status',)
