# Generated by Django 5.0.6 on 2024-08-04 17:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0029_alter_public_cart_product_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='public_reviews',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=2000)),
                ('customer_fullname', models.CharField(max_length=160)),
                ('product_id', models.IntegerField()),
                ('product_sec_id', models.UUIDField()),
                ('customer_rating', models.CharField(choices=[('5', '★★★★★'), ('4', '★★★★'), ('3', '★★★'), ('2', '★★'), ('1', '★')], max_length=10)),
                ('customer_feedback', models.TextField(max_length=2000)),
            ],
        ),
    ]
