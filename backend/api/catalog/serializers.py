from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from catalog.models import Brand, Product, ProductImages
from users.models import Supplier


class BrandSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name',)
        model = Brand


class ProductImagesSerializer(serializers.ModelSerializer):
    images = Base64ImageField(required=False)

    class Meta:
        fields = (
            'images',
            )
        model = ProductImages


class ProductWriteSerializer(serializers.ModelSerializer):

    brand = serializers.PrimaryKeyRelatedField(
        queryset=Brand.objects.all(),
        label='Brands',
    )
    supplier = serializers.PrimaryKeyRelatedField(
        queryset=Supplier.objects.all(),
        label='Suppliers',
    )
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
            'specification_file',
        )
        model = Product


class ProductReadSerializer(serializers.ModelSerializer):

    brand = serializers.ReadOnlyField(source='brand.name')
    supplier = serializers.ReadOnlyField(source='supplier.name')
    images = ProductImagesSerializer(many=True, source='product_images')

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
            'images',
            'specification_file',
        )
        model = Product
