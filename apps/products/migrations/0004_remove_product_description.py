# Generated by Django 3.2.13 on 2024-09-30 17:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('apps_products', '0003_product_deleted_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='description',
        ),
    ]
