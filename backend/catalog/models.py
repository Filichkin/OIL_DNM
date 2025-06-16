from django.core.validators import MinValueValidator
from django.db import models

from .constants import (
    PACKAGE_COUNT_MIN,
    PRODUCT_DESCRIPTION_MAX_LENGTH,
    PRODUCT_SPECIFICATION_MAX_LENGTH,
    PRODUCT_NAME_MAX_LENGTH,
    VOLUME_LITRES_MIN
)


class Product(models.Model):
    name = models.CharField(
        max_length=PRODUCT_NAME_MAX_LENGTH,
        unique=True,
        verbose_name='Product name',
    )
    part_number = models.CharField(
        unique=True,
        verbose_name='Part number',
    )
    brand = models.CharField(
        verbose_name='Brand name',
    )
    package_count = models.PositiveSmallIntegerField(
        validators=(MinValueValidator(
            PACKAGE_COUNT_MIN,
            f'Can not be less than {PACKAGE_COUNT_MIN} units!'
        ),),
        verbose_name='Package units count',
    )
    volume = models.PositiveSmallIntegerField(
        validators=(MinValueValidator(
            VOLUME_LITRES_MIN,
            f'Can not be less than {VOLUME_LITRES_MIN} litres!'
        ),),
        verbose_name='Voulume in litres',
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Price'
        )
    description = models.CharField(
        max_length=PRODUCT_DESCRIPTION_MAX_LENGTH,
        verbose_name='Product description',
    )
    specification = models.CharField(
        max_length=PRODUCT_SPECIFICATION_MAX_LENGTH,
        verbose_name='Product specification',
    )
    image = models.ImageField(
        upload_to='media/product_image/',
        verbose_name='Product image',
        null=True,
        blank=True
        )
    specification_file = models.FileField(
        upload_to='media/product_specification_file/',
        verbose_name='Product specification file',
        null=True,
        blank=True
        )
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата и время размещения'
        )
    updated = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата и время обновления'
        )

    class Meta:
        ordering = ['brand']
        indexes = [
            models.Index(fields=['id']),
            models.Index(fields=['name']),
            models.Index(fields=['-created']),
        ]
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    def __str__(self):
        return self.name
