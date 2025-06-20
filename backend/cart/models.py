from django.db import models

from catalog.models import Catalog
from users.models import Dealer


class Cart(Catalog):

    class Meta:
        verbose_name = 'Cart'

    def __str__(self):
        return self.name


class Order(models.Model):
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

    class Meta:
        ordering = ('-id',)

    def __str__(self):
        return self.id
