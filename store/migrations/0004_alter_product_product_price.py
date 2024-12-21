# Generated by Django 5.0.6 on 2024-08-22 07:13

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("store", "0003_alter_product_product_price"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="product_price",
            field=models.DecimalField(decimal_places=4, default=0, max_digits=6),
        ),
    ]
