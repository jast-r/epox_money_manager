# -*- encoding: utf-8 -*-

from django.urls import path, re_path
from apps.clients.views import ClientView, Clients

urlpatterns = [
    path('clients/', Clients, name='clients_list'),
    re_path(r'^api/clients/(?:(?P<pk>\d+)/)?(?:(?P<action>\w+)/)?', ClientView.as_view(), name='clients'),
]
