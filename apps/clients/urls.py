# -*- encoding: utf-8 -*-

from django.urls import path, re_path
import apps.clients.views as views

urlpatterns = [
    path('clients/', views.Clients, name='clients_list'),
    re_path(r'^api/clients/(?:(?P<pk>\d+)/)?(?:(?P<action>\w+)/)?', views.ClientView.as_view(), name='api/clients'),
]
