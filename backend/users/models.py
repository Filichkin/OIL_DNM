from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from .constants import (
    CITY_MAX_LENGTH,
    DEALER_NAME_MAX_LENGTH,
    DESCRIPTION_MAX_LENGTH,
    EMAIL_MAX_LENGTH,
    FIRST_NAME_MAX_LENGTH,
    JOB_TITLE_MAX_LENGTH,
    LAST_NAME_MAX_LENGTH,
    ADDRESS_MAX_LENGTH,
    SUPPLIER_NAME_MAX_LENGTH,
    USERNAME_MAX_LENGTH
)
from .validators import validate_dealer_code, validate_inn


class Dealer(models.Model):
    rs_code = models.CharField(
        verbose_name='Dealer RS code',
        validators=(validate_dealer_code,)
    )
    name = models.CharField(
        max_length=DEALER_NAME_MAX_LENGTH,
        unique=True,
        verbose_name='Unique dealer name',
    )
    inn = models.BigIntegerField(
        verbose_name='Dealer INN',
        validators=(validate_inn,)
    )
    city = models.CharField(
        max_length=CITY_MAX_LENGTH,
        verbose_name='Dealer city name',
    )
    address = models.CharField(
        max_length=ADDRESS_MAX_LENGTH,
        verbose_name='Dealer address',
    )
    legal_address = models.CharField(
        max_length=ADDRESS_MAX_LENGTH,
        verbose_name='Dealer legal address',
    )
    delivery_time = models.PositiveSmallIntegerField(
        verbose_name='Delivery time to dealer',
        default=1
    )
    transport_size_limitation = models.CharField(
        max_length=DESCRIPTION_MAX_LENGTH,
        verbose_name='Transport size limitation',
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = 'Dealer'
        verbose_name_plural = 'Dealers'
        ordering = ['id']

    def __str__(self):
        return self.rs_code


class Supplier(models.Model):
    name = models.CharField(
        max_length=SUPPLIER_NAME_MAX_LENGTH,
        unique=True,
        verbose_name='Unique supplier name',
    )
    legal_name = models.CharField(
        max_length=SUPPLIER_NAME_MAX_LENGTH,
        unique=True,
        verbose_name='Unique supplier legal name',
    )
    inn = models.BigIntegerField(
        verbose_name='Supplier INN',
        validators=(validate_inn,)
    )
    phone = PhoneNumberField(region='RU', blank=False)
    contact_name = models.CharField(
        max_length=LAST_NAME_MAX_LENGTH,
    )
    contact_job_title = models.CharField(
        max_length=JOB_TITLE_MAX_LENGTH,
        verbose_name='Contact job title',
    )
    address = models.CharField(
        max_length=ADDRESS_MAX_LENGTH,
        verbose_name='Supplier address',
    )
    legal_address = models.CharField(
        max_length=ADDRESS_MAX_LENGTH,
        verbose_name='Supplier legal address',
    )

    class Meta:
        verbose_name = 'Supplier'
        verbose_name_plural = 'Suppliers'
        ordering = ['id']

    def __str__(self):
        return self.name


class User(AbstractUser):
    username = models.CharField(
        max_length=USERNAME_MAX_LENGTH,
        unique=True,
        validators=(UnicodeUsernameValidator(),),
        verbose_name='Unique username',
    )
    email = models.EmailField(
        max_length=EMAIL_MAX_LENGTH,
        unique=True,
        verbose_name='Email address',
    )
    first_name = models.CharField(
        max_length=FIRST_NAME_MAX_LENGTH,
    )
    last_name = models.CharField(
        max_length=LAST_NAME_MAX_LENGTH,
    )
    phone = PhoneNumberField(region='RU', blank=False)
    rs_code = models.ForeignKey(
        Dealer,
        on_delete=models.SET_NULL,
        related_name='dealer_users',
        blank=True,
        null=True,
        )
    supplier = models.ForeignKey(
        Supplier,
        on_delete=models.SET_NULL,
        related_name='supplier_users',
        blank=True,
        null=True,
        )
    is_distributor = models.BooleanField(default=False)
    is_supplier = models.BooleanField(default=False)
    is_dealer = models.BooleanField(default=False)
    is_dealer_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = (
        'username',
        'first_name',
        'last_name',
    )

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['id']

    def __str__(self):
        return self.email
