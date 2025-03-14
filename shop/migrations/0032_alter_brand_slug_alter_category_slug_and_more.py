# Generated by Django 5.1.5 on 2025-01-24 11:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0031_product_updated_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='brand',
            name='slug',
            field=models.SlugField(unique=True),
        ),
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(unique=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='slug',
            field=models.SlugField(unique=True),
        ),
        migrations.AlterField(
            model_name='shop',
            name='slug',
            field=models.SlugField(unique=True),
        ),
        migrations.AlterField(
            model_name='subcategory',
            name='slug',
            field=models.SlugField(unique=True),
        ),
    ]
