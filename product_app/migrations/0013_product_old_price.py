# Generated by Django 5.2 on 2025-04-15 10:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product_app', '0012_remove_product_old_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='old_price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]
