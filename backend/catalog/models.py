from django.core.validators import (
    FileExtensionValidator,
    MinValueValidator
)
from django.db import models

from .constants import (
    PACKAGE_COUNT_MIN,
    PRODUCT_DESCRIPTION_MAX_LENGTH,
    PRODUCT_SPECIFICATION_MAX_LENGTH,
    PRODUCT_NAME_MAX_LENGTH,
    VOLUME_LITRES_MIN
)
from users.constants import SUPPLIER_NAME_MAX_LENGTH
from users.models import Supplier


class Catalog(models.Model):
    supplier = models.CharField(
        max_length=SUPPLIER_NAME_MAX_LENGTH,
        unique=True,
        verbose_name='Supplier name',
    )
    brand = models.CharField(
        verbose_name='Brand name',
    )
    name = models.CharField(
        max_length=PRODUCT_NAME_MAX_LENGTH,
        unique=True,
        verbose_name='Product name',
    )
    part_number = models.CharField(
        unique=True,
        verbose_name='Part number',
    )
    volume = models.PositiveSmallIntegerField(
        validators=(MinValueValidator(
            VOLUME_LITRES_MIN,
            f'Can not be less than {VOLUME_LITRES_MIN} litres!'
        ),),
        verbose_name='Volume in litres',
    )
    price_per_litre = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Price for litre'
        )
    price_per_box = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Price for box'
        )
    avalible_count = models.PositiveSmallIntegerField(
        verbose_name='Avalible count',
    )
    transit_count = models.PositiveSmallIntegerField(
        verbose_name='Avalible in transit',
    )
    arrival_date = models.DateTimeField(
        verbose_name='Estimated arrival date'
        )
    updated_date = models.DateTimeField(
        verbose_name='Date of count and transit updated'
        )

    class Meta:
        ordering = ['brand']
        indexes = [
            models.Index(fields=['id']),
            models.Index(fields=['name']),
        ]
        verbose_name = 'Catalog'
        verbose_name_plural = 'Catalog'

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(
        verbose_name='Brand name',
    )

    class Meta:
        verbose_name = 'Brand'
        verbose_name_plural = 'Brands'

    def __str__(self):
        return self.name


class Product(models.Model):
    supplier = models.ForeignKey(
        Supplier,
        on_delete=models.CASCADE,
        related_name='products',
        blank=False,
        null=False,
        )
    name = models.CharField(
        max_length=PRODUCT_NAME_MAX_LENGTH,
        unique=True,
        verbose_name='Product name',
    )
    part_number = models.CharField(
        unique=True,
        verbose_name='Part number',
        primary_key=True
    )
    brand = models.ForeignKey(
        Brand,
        on_delete=models.CASCADE,
        related_name='products',
        blank=False,
        null=False,
        verbose_name='Brand name'
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
        verbose_name='Volume in litres',
    )
    price_per_box = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Price for box'
        )
    description = models.CharField(
        max_length=PRODUCT_DESCRIPTION_MAX_LENGTH,
        verbose_name='Product description',
    )
    specification = models.CharField(
        max_length=PRODUCT_SPECIFICATION_MAX_LENGTH,
        verbose_name='Product specification',
    )
    specification_file = models.FileField(
        upload_to='media/product_specification_file/',
        verbose_name='Product specification file',
        null=True,
        blank=True
        )

    class Meta:
        ordering = ['supplier']
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    def __str__(self):
        return self.name


def product_image_upload_to(instance, filename):
    return f'product_images/{instance.product.part_number}/{filename}'


class ProductImages(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        null=True,
        related_name='product_images'
        )
    image = models.ImageField(
        upload_to=product_image_upload_to,
        validators=[FileExtensionValidator(['png', 'jpg', 'jpeg', 'gif'])],
        verbose_name='Product image',
        null=True,
        blank=True
        )

    class Meta:
        verbose_name = 'Product image'

    def __str__(self):
        return self.product.name
