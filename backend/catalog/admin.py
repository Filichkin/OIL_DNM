from django.contrib import admin

from catalog.models import Brand, Catalog, Product


@admin.register(Catalog)
class CatalogAdmin(admin.ModelAdmin):
    list_display = (
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
        )
    search_fields = ('name', 'part_number',)


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        )
    search_fields = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'supplier',
        'name',
        'part_number',
        'brand',
        'package_count',
        'volume',
        'price_per_unit',
        'description',
        'specification'
        )
    search_fields = ('name', 'part_number',)
