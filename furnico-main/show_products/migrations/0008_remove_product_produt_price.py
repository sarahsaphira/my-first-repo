# Generated by Django 5.1.1 on 2024-10-22 13:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('show_products', '0007_product_product_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='produt_price',
        ),
    ]
