# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from clients import views

urlpatterns = [
    re_path(r'^cients/(?:(?P<pk>\d+)/)?(?:(?P<action>\w+)/)?', views.OrderView.as_view(), name='orders'),
]
