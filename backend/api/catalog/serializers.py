from rest_framework import serializers

from catalog.models import Brand, Product, Supplier


class ProductWriteSerializer(serializers.ModelSerializer):
    """
    Сериализатор только для записи данных.
    Возвращает JSON-данные всех полей модели Product
    для эндпоинта api/products/.
    """

    brand = serializers.PrimaryKeyRelatedField(
        queryset=Brand.objects.all(),
        label='Brands',
    )
    supplier = serializers.PrimaryKeyRelatedField(
        queryset=Supplier.objects.all(),
        label='Suppliers',
    )

    class Meta:
        fields = (
            'id',
            'brand',
            'supplier'
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
