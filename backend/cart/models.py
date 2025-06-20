from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from catalog.models import Catalog
from .constants import MAX_CART_COUNT, MIN_CART_COUNT
from users.models import Dealer


class Cart(models.Model):
    dealer = models.ForeignKey(
        Dealer,
        on_delete=models.CASCADE,
        related_name='dealer_orders',
        verbose_name='Dealer',
    )
    product = models.ForeignKey(
        Catalog,
        on_delete=models.CASCADE,
        verbose_name='prodect_orders',
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

    class Meta:
        verbose_name = 'Cart'

    def __str__(self):
        return str(self.id)
