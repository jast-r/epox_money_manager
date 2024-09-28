# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from apps.orders import views

urlpatterns = [
    path('order/', views.Orders, name='orders_list'),
    re_path(r'^api/order/(?:(?P<pk>\d+)/)?(?:(?P<action>\w+)/)?', views.OrderView.as_view(), name='api/orders'),
]
