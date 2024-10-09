# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.db import models
from apps.products.models import Product
from django.utils import timezone
from django.db.models import Sum, F, ExpressionWrapper, FloatField, Count
from django.db.models.functions import TruncDate
from django.utils import timezone
from datetime import datetime, time
from django.utils import timezone

# Create your models here.

class Order(models.Model):
    class Priority(models.IntegerChoices):
        NOT_URGENT = 1, "Не срочно"
        MEDIUM = 2, "Средне"
        URGENT = 3, "Срочно"

    class Status(models.IntegerChoices):
        ACCEPTED = 1, "Принят"
        IN_PROGRESS = 2, "В процессе"
        DONE = 3, "Выполнен"

    id = models.AutoField(primary_key=True)
    client_fio = models.CharField(max_length=100, null=True, blank=True)
    client_tg = models.CharField(max_length=100, null=True, blank=True)
    client_phone = models.CharField(max_length=100, null=True, blank=True)
    product = models.ForeignKey(Product, null=False, on_delete=models.CASCADE)
    quantity = models.IntegerField(null=False, blank=False)
    sell_price = models.FloatField(null=False, blank=False)
    address = models.TextField(null=False, blank=False)
    description = models.TextField(null=True, blank=True)
    priority = models.IntegerField(choices=Priority.choices, default=Priority.NOT_URGENT)
    status = models.IntegerField(choices=Status.choices, default=Status.ACCEPTED)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = "apps_orders"
        verbose_name = "order"
        verbose_name_plural = "orders"

    @classmethod
    def _get_date_range(cls, period, default_days):
        """Вспомогательный метод для получения диапазона дат"""
        end_date = timezone.now()
        start_date = end_date - datetime.timedelta(days=default_days)
        return start_date, end_date

    @classmethod
    def _aggregate_data(cls, start_date, end_date):
        """Общий метод для агрегации данных"""
        base_query = cls.objects.filter(
            created_at__gte=start_date,
            created_at__lte=datetime.combine(end_date, time.max),
            deleted_at=None
        )

        res = base_query.annotate(
                    item_profit=F('sell_price') - F('product__price') * F('quantity'),
                    created_at_date=TruncDate('created_at')
                ).values('created_at_date').annotate(
                    revenue=Sum('sell_price'),
                    profit=Sum('item_profit'),
                    orders_count=Count('client_phone'),
                    customers_count=Count('client_phone', distinct=True)
                ).order_by('created_at_date')\
                        
        return res

    @classmethod
    def _get_data_for_period(cls, start_date=None, end_date=None):
        return cls._aggregate_data(start_date, end_date)