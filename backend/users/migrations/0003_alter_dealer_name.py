# Generated by Django 5.0.14 on 2025-06-14 14:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0002_alter_dealer_inn_alter_dealer_rs_code_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="dealer",
            name="name",
            field=models.CharField(
                max_length=150, unique=True, verbose_name="Unique dealer name"
            ),
        ),
    ]
