# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from apps.products import views

urlpatterns = [
    path('products/', views.Products, name='products_list'),
    re_path(r'^api/products/(?:(?P<pk>\d+)/)?(?:(?P<action>\w+)/)?', views.ProductView.as_view(), name='api/products'),
]
