from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from catalog.models import Brand, Product, ProductImages
from users.models import Supplier


class BrandSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name',)
        model = Brand


class ProductImagesSerializer(serializers.ModelSerializer):
    image = Base64ImageField(required=False)

    class Meta:
        fields = (
            'image',
            )
        model = ProductImages


class ProductCreateSerializer(serializers.ModelSerializer):

    brand = serializers.PrimaryKeyRelatedField(
        queryset=Brand.objects.all(),
        label='Brands',
    )
    supplier = serializers.PrimaryKeyRelatedField(
        queryset=Supplier.objects.all(),
        label='Suppliers',
    )
    specification_file = serializers.FileField(required=False)
    images = serializers.ListField(
        child=Base64ImageField(required=False),
        min_length=0,
        write_only=True,
        required=False,
    )

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
            'images'
        )
        model = Product

    def create(self, validated_data):
        images = validated_data.pop('images')
        brand = validated_data.pop('brand')
        supplier = validated_data.pop('supplier')
        product = Product.objects.create(
            brand=brand,
            supplier=supplier,
            **validated_data
        )
        if images:
            for image in images:
                ProductImages.objects.create(
                    product=product,
                    image=image,
                )
        return product


class ProductReadSerializer(serializers.ModelSerializer):

    brand = serializers.ReadOnlyField(source='brand.name')
    supplier = serializers.ReadOnlyField(source='supplier.name')
    images = ProductImagesSerializer(
        many=True,
        read_only=True,
        source='product_images'
        )

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
