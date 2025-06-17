from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from catalog.models import Brand, Product, Supplier


class BrandSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name',)
        model = Brand


class ProductWriteSerializer(serializers.ModelSerializer):

    brand = serializers.PrimaryKeyRelatedField(
        queryset=Brand.objects.all(),
        label='Brands',
    )
    supplier = serializers.PrimaryKeyRelatedField(
        queryset=Supplier.objects.all(),
        label='Suppliers',
    )
    image = Base64ImageField(required=False)
    specification_file = serializers.FileField(required=False)

    class Meta:
        fields = (
            'brand',
            'supplier',
            'name',
            'part_number',
            'package_count',
            'volume',
            'price_per_unit',
            'description',
            'specification',
            'image',
            'specification_file',
        )
        model = Product


class ProductReadSerializer(serializers.ModelSerializer):
    brand = serializers.ReadOnlyField(source='brand.name')
    supplier = serializers.ReadOnlyField(source='supplier.name')

    class Meta:
        fields = (
            'brand',
            'supplier',
            'name',
            'part_number',
            'package_count',
            'volume',
            'price_per_unit',
            'description',
            'specification',
        )
        model = Product
