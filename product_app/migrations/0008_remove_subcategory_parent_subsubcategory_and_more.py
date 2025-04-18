# Generated by Django 5.1.7 on 2025-03-25 18:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product_app', '0007_subcategory_parent_alter_subcategory_category'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subcategory',
            name='parent',
        ),
        migrations.CreateModel(
            name='SubSubcategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('subcategory', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='product_app.subcategory')),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='sub_subcategory',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='product_app.subsubcategory'),
        ),
    ]
