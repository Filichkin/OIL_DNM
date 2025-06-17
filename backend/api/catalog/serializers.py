from rest_framework import serializers

from catalog.models import Product


class ProductWriteSerializer(serializers.ModelSerializer):
    """
    Сериализатор только для записи данных.
    Возвращает JSON-данные всех полей модели Product
    для эндпоинта api/products/.
    """

    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True
    )

    class Meta:
        fields = (
            'id',
            'name',
            'year',
            'description',
            'genre',
            'category'
        )
        model = Title