from django.contrib import admin

from catalog.models import Product


@admin.register(Product)
class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'part_number',
        'brand',
        'package_count',
        'volume',
        'price',
        'description',
        'specification',
        )
    search_fields = ('name', 'part_number',)
