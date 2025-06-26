from django.db import models

from api.catalog.constants import DECIMAL_PLACES, MAX_DIGITS
from catalog.models import Catalog


class OrderStatus(models.TextChoices):
    NEW = 'new'
    CONFIRMED = 'confirmed'
    IN_WORK = 'in_work'
    CANCELED = 'canceled'
    DELIVERED = 'delivered'


class Order(models.Model):
    order_number = models.CharField()
    dealer_name = models.CharField()
    rs_code = models.CharField()

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
    delivery_date = models.DateTimeField()
    comment = models.CharField()

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
        if not self.order_number:
            self.order_number = str(self.rs_code) + str(self.id)
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
