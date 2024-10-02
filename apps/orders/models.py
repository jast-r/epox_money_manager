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