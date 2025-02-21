# Generated by Django 3.2.13 on 2024-10-01 22:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('apps_products', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('client_fio', models.CharField(blank=True, max_length=100, null=True)),
                ('client_tg', models.CharField(blank=True, max_length=100, null=True)),
                ('client_phone', models.CharField(blank=True, max_length=100, null=True)),
                ('quantity', models.IntegerField()),
                ('sell_price', models.FloatField()),
                ('address', models.TextField()),
                ('description', models.TextField(blank=True, null=True)),
                ('priority', models.IntegerField(choices=[(1, 'Не срочно'), (2, 'Средне'), (3, 'Срочно')], default=1)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apps_products.product')),
            ],
            options={
                'verbose_name': 'order',
                'verbose_name_plural': 'orders',
                'db_table': 'apps_orders',
            },
        ),
    ]
