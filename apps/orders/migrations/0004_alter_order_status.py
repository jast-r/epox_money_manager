# Generated by Django 3.2.13 on 2024-10-28 04:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apps_orders', '0003_alter_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.IntegerField(choices=[(1, 'Принят'), (2, 'В процессе'), (3, 'Доставка'), (4, 'Выполнен')], default=1),
        ),
    ]
