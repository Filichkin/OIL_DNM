# Generated by Django 5.0.14 on 2025-06-18 17:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("catalog", "0003_alter_productimages_options_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="product",
            old_name="price_per_unit",
            new_name="price_per_box",
        ),
    ]
