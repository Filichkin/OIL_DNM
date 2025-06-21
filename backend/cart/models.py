from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from catalog.models import Catalog
from .constants import MAX_CART_COUNT, MIN_CART_COUNT
from users.models import Dealer


class OrderList(models.Model):
    dealer = models.ForeignKey(
        Dealer,
        on_delete=models.CASCADE,
        related_name='orders',
        null=True,
        blank=True
        )
    product = models.ForeignKey(
        Catalog,
        on_delete=models.CASCADE,
        verbose_name='Product_orders',
        related_name='orders',
        null=True,
        blank=True
    )
    count = models.PositiveSmallIntegerField(
        verbose_name='Count',
        validators=[
            MinValueValidator(MIN_CART_COUNT),
            MaxValueValidator(MAX_CART_COUNT)
            ],
        null=False,
        blank=False
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'OrderList'

    def __str__(self):
        return f'Order({self.id})'
