from datetime import datetime, timedelta

from django.db import models
from django.utils.timezone import get_current_timezone

from api.catalog.constants import DECIMAL_PLACES, MAX_DIGITS
from orders.constants import COMMENT_MAX_LENGTH
from catalog.models import Catalog
from users.models import Dealer


class OrderStatus(models.TextChoices):
    NEW = 'new'
    CONFIRMED = 'confirmed'
    IN_WORK = 'in_work'
    CANCELED = 'canceled'
    DELIVERED = 'delivered'


class Order(models.Model):
    order_number = models.CharField(
        verbose_name='Order number',
        blank=True,
        null=True,
        unique=True
    )
    dealer = models.ForeignKey(
        Dealer,
        on_delete=models.CASCADE,
        related_name='orders',
        blank=False,
        null=False,
        )

    created = models.DateTimeField(
        auto_now_add=True,
    )
    updated = models.DateTimeField(
        auto_now=True,
        )
    status = models.CharField(
        choices=OrderStatus.choices,
        default=OrderStatus.NEW,
        verbose_name='Order status'
    )
    delivery_date = models.DateTimeField(
        verbose_name='Order delivery date',
        blank=True,
        null=True,
    )
    comment = models.CharField(
        verbose_name='Order comment',
        blank=True,
        null=True,
        max_length=COMMENT_MAX_LENGTH
    )

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created'])
        ]
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

    def __str__(self):
        return f'Order {self.id}'

    def save(self, *args, **kwargs):
        if not self.delivery_date:
            self.delivery_date = (
                datetime.now(tz=get_current_timezone()) + timedelta(days=3)
                )
        super().save(*args, **kwargs)

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        related_name='items',
        on_delete=models.CASCADE,
        verbose_name='Order'
    )
    product = models.ForeignKey(
        Catalog,
        related_name='order_items',
        on_delete=models.CASCADE,
        verbose_name='Product'
    )
    price = models.DecimalField(
        max_digits=MAX_DIGITS,
        decimal_places=DECIMAL_PLACES,
        verbose_name='Price'
    )
    count = models.PositiveIntegerField(
        verbose_name='Count'
        )

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return self.price * self.count
