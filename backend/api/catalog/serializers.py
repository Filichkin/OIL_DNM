from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from api.catalog.constants import DECIMAL_PLACES, MAX_DIGITS
from cart.models import OrderList
from catalog.models import Brand, Catalog, Product, ProductImages
from users.models import Dealer, Supplier


class BrandSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name',)
        model = Brand


class CatalogReadSerializer(serializers.ModelSerializer):
    supplier = serializers.ReadOnlyField()

    class Meta:
        fields = (
            'id',
            'supplier',
            'brand',
            'name',
            'part_number',
            'volume',
            'price_per_litre',
            'price_per_box',
            'avalible_count',
            'transit_count',
            'arrival_date',
            'updated_date',
            'specification',
            )
        model = Catalog


class CatalogCreateSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'id',
            'brand',
            'name',
            'part_number',
            'volume',
            'price_per_litre',
            'price_per_box',
            'avalible_count',
            'transit_count',
            'arrival_date',
            'updated_date',
            'specification',
            )
        model = Catalog

    def update(self, instance, validated_data):
        instance.price_per_litre = validated_data.get(
            'price_per_litre',
            instance.price_per_litre
            )
        instance.price_per_box = validated_data.get(
            'price_per_box',
            instance.price_per_box
            )
        instance.avalible_count = validated_data.get(
            'avalible_count',
            instance.avalible_count
            )
        instance.transit_count = validated_data.get(
            'transit_count',
            instance.transit_count
            )
        instance.arrival_date = validated_data.get(
            'arrival_date',
            instance.arrival_date
            )
        instance.updated_date = validated_data.get(
            'updated_date',
            instance.updated_date
            )
        return super().update(instance, validated_data)


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
            'price_per_box',
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
            'price_per_box',
            'description',
            'specification',
            'images',
            'specification_file',
        )
        model = Product


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderList
        fields = (
            'id',
            'order',
            'product',
            'count',
            'created_at',
            'updated_at'
            )
        read_only_fields = ('id', 'created_at', 'updated_at')


class OrderCreateSerializer(serializers.ModelSerializer):
    dealer = serializers.PrimaryKeyRelatedField(
        queryset=Dealer.objects.all(),
        label='Dealer'
    )
    product = serializers.PrimaryKeyRelatedField(
        queryset=Catalog.objects.all(),
        label='Products'
    )
    count = serializers.IntegerField()

    class Meta:
        model = OrderList
        fields = (
            'id',
            'dealer',
            'product',
            'count'
            )
        read_only_fields = ('id',)


class CartItemSerializer(serializers.Serializer):
    count = serializers.IntegerField(min_value=1)
    dealer = serializers.PrimaryKeyRelatedField(
        queryset=Dealer.objects.all(),
        label='Dealer'
    )


class CartItemDeleteSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    dealer = serializers.PrimaryKeyRelatedField(
        queryset=Dealer.objects.all(),
        label='Dealer'
    )


class CartContentSerializer(serializers.Serializer):
    dealer = serializers.ReadOnlyField()
    product_id = serializers.IntegerField()
    product_name = serializers.CharField()
    brand = serializers.CharField()
    part_number = serializers.CharField()
    volume = serializers.CharField()
    count = serializers.IntegerField()
    price_per_box = serializers.DecimalField(
        max_digits=MAX_DIGITS,
        decimal_places=DECIMAL_PLACES
        )
    total_price = serializers.DecimalField(
        max_digits=MAX_DIGITS,
        decimal_places=DECIMAL_PLACES
        )
