from django.contrib import admin

from cart.models import OrderList


@admin.register(OrderList)
class OrderListAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'dealer',
        'product',
        'count',
        'created_at',
        'updated_at'
        )
    search_fields = ('product',)
