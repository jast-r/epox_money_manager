# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from apps.orders import views

urlpatterns = [
    path('orders/', views.Orders, name='orders_list'),
    path('api/orders/total-info/', views.get_total_info, name='get_total_info'),
    path('api/orders/<int:order_id>/status/', views.update_order_status, name='update_order_status'),
    re_path(r'^api/orders/(?:(?P<pk>\d+)/)?(?:(?P<action>\w+)/)?', views.OrderView.as_view(), name='api/orders'),
]
