# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.db import models
from apps.clients.models import Client
from apps.products.models import Product

# Create your models here.

class Order(models.Model):
    PRIORITIES = {
        1: "Не срочно",
        2: "Средне",
        3: "Срочно",
    }

    ID = models.AutoField(primary_key=True)
    client = models.ForeignKey(Client, null=True, on_delete=models.SET_NULL)
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
    quantity = models.IntegerField(null=False, blank=False)
    sell_price = models.FloatField(null=False, blank=False)
    address = models.TextField(null=False, blank=False)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    priority = models.IntegerField(null=False, blank=False)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = "apps_orders"
        verbose_name = "order"
        verbose_name_plural = "orders"