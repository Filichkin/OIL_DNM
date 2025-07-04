from django.contrib import admin

from catalog.models import Brand, Catalog, Product, ProductImages


@admin.register(Catalog)
class CatalogAdmin(admin.ModelAdmin):
    list_display = (
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
        'specification'
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
        'price_per_box',
        'description',
        'specification'
        )
    search_fields = ('name', 'part_number',)


@admin.register(ProductImages)
class ProductImagesAdmin(admin.ModelAdmin):
    list_display = (
        'product',
        'image',
        )
