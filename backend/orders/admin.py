from django.contrib import admin

from orders.models import Order, OrderItem


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'order_number',
        'rs_code',
        'created',
        'status',
        'delivery_date',
        'comment'
        )
    search_fields = ('order_number', 'rs_code',)


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'order',
        'product',
        'price',
        'count',
        )
    search_fields = ('id',)
