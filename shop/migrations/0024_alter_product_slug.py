# Generated by Django 4.2.6 on 2024-05-01 01:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0023_alter_product_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='slug',
            field=models.SlugField(default='Optional-Field', unique=True, verbose_name='djangodbmodelsfieldscharfield'),
        ),
    ]
