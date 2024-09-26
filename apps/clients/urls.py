# -*- encoding: utf-8 -*-

from django.urls import path, re_path
from apps.clients.views import ClientView

urlpatterns = [
    re_path(r'^clients/(?:(?P<pk>\d+)/)?(?:(?P<action>\w+)/)?', ClientView.as_view(), name='clients'),
]
