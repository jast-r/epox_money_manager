# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.db import models
from apps.clients.models import Client
from apps.products.models import Product
from django.utils import timezone
from django.db.models import Sum, F, ExpressionWrapper, FloatField

# Create your models here.

class Order(models.Model):
    class Priority(models.IntegerChoices):
        NOT_URGENT = 1, "Не срочно"
        MEDIUM = 2, "Средне"
        URGENT = 3, "Срочно"

    id = models.AutoField(primary_key=True)
    client = models.ForeignKey(Client, null=True, on_delete=models.SET_NULL)
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
    quantity = models.IntegerField(null=False, blank=False)
    sell_price = models.FloatField(null=False, blank=False)
    address = models.TextField(null=False, blank=False)
    description = models.TextField(null=True, blank=True)
    priority = models.IntegerField(choices=Priority.choices, default=Priority.NOT_URGENT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = "apps_orders"
        verbose_name = "order"
        verbose_name_plural = "orders"

    @classmethod
    def today_orders(cls):
        # Получаем локальное время для начала и конца текущего дня
        local_now = timezone.localtime()
        start_of_day = local_now.replace(hour=0, minute=0, second=0, microsecond=0)
        end_of_day = local_now.replace(hour=23, minute=59, second=59, microsecond=999999)
        
        result = cls.objects.filter(
            created_at__range=(start_of_day, end_of_day),
            deleted_at=None
        ).count()
        
        return result
    
    @classmethod
    def today_revenue(cls):
        # Получаем локальное время для начала и конца текущего дня
        local_now = timezone.localtime()
        start_of_day = local_now.replace(hour=0, minute=0, second=0, microsecond=0)
        end_of_day = local_now.replace(hour=23, minute=59, second=59, microsecond=999999)

        result = cls.objects.filter(
            created_at__range=(start_of_day, end_of_day),
            deleted_at=None
        ).aggregate(today_revenue=Sum('sell_price'))
        
        return result.get('today_revenue', 0.0)  # Вернуть 0.0, если нет данных
    
    @classmethod
    @classmethod
    def today_profit(cls):
        # Получаем локальное время для начала и конца текущего дня
        local_now = timezone.localtime()
        start_of_day = local_now.replace(hour=0, minute=0, second=0, microsecond=0)
        end_of_day = local_now.replace(hour=23, minute=59, second=59, microsecond=999999)

        # Рассчитываем прибыль как sell_price - product.price * quantity
        profit_expr = ExpressionWrapper(
            F('sell_price') - F('product__price') * F('quantity'),
            output_field=FloatField()
        )
        
        result = cls.objects.filter(
            created_at__range=(start_of_day, end_of_day),
            deleted_at=None
        ).aggregate(today_profit=Sum(profit_expr))
        
        return result.get('today_profit', 0.0)  # Вернуть 0.0, если данных нет