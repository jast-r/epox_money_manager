# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.db import models
from django.utils import timezone
from django.db.models import Sum, F, ExpressionWrapper, FloatField

# Create your models here.

class Client(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    tg_username = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "apps_clients"
        verbose_name = "client"
        verbose_name_plural = "clients"

    @classmethod
    def today_clients(cls):
        # Получаем локальное время для начала и конца текущего дня
        now = timezone.now()
        start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
        end_of_day = now.replace(hour=23, minute=59, second=59, microsecond=999999)
        
        result = cls.objects.filter(
            created_at__range=(start_of_day, end_of_day),
            deleted_at=None
        ).count()
        
        return result

    