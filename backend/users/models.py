from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from .constants import (
    DEALER_NAME_MAX_LENGTH,
    EMAIL_MAX_LENGTH,
    FIRST_NAME_MAX_LENGTH,
    JOB_TITLE_MAX_LENGTH,
    LAST_NAME_MAX_LENGTH,
    ROLE_MAX_LENGTH,
    SUPPLIER_ADDRESS_MAX_LENGTH,
    SUPPLIER_NAME_MAX_LENGTH
)
from .validators import validate_dealer_code, validate_inn


class UserRole(models.TextChoices):
    DEALER = 'is_dealer'
    SUPPLIER = 'is_supplier'
    DISTRIBUTOR = 'is_distributor'


class User(AbstractUser):
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
    role = models.CharField(
        choices=UserRole.choices,
        max_length=ROLE_MAX_LENGTH,
        default=UserRole.DEALER,
        verbose_name='Role'
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = (
        'first_name',
        'last_name',
    )

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['id']

    def __str__(self):
        return self.email

    @property
    def is_distributor(self):
        return (
            self.role == UserRole.DISTRIBUTOR
            or self.is_superuser
            or self.is_staff
        )

    @property
    def is_supplierr(self):
        return self.role == UserRole.SUPPLIER


class Dealer(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='dealer_users',
        verbose_name='Dealer user',
    )
    rs_code = models.SmallIntegerField(
        verbose_name='Dealer RS code',
        validators=(validate_dealer_code,),
    )
    name = models.CharField(
        max_length=DEALER_NAME_MAX_LENGTH,
        unique=True,
        validators=(UnicodeUsernameValidator(),),
        verbose_name='Unique dealer name',
    )
    inn = models.SmallIntegerField(
        verbose_name='Dealer INN',
        validators=(validate_inn,)
    )
    phone = PhoneNumberField(region='RU', blank=False)

    def __str__(self):
        return self.code


class Supplier(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='supplier_users',
        verbose_name='Supplier user',
    )
    name = models.CharField(
        max_length=SUPPLIER_NAME_MAX_LENGTH,
        unique=True,
        validators=(UnicodeUsernameValidator(),),
        verbose_name='Unique supplier name',
    )
    legal_name = models.CharField(
        max_length=SUPPLIER_NAME_MAX_LENGTH,
        unique=True,
        validators=(UnicodeUsernameValidator(),),
        verbose_name='Unique supplier legal name',
    )
    inn = models.SmallIntegerField(
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
        max_length=SUPPLIER_ADDRESS_MAX_LENGTH,
        verbose_name='Supplier address',
    )
    legal_address = models.CharField(
        max_length=SUPPLIER_ADDRESS_MAX_LENGTH,
        verbose_name='Supplier legal address',
    )

    def __str__(self):
        return self.name
