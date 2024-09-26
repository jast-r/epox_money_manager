# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib import admin
from django.urls import path, include  # add this

urlpatterns = [
    path('admin/', admin.site.urls),          # Django admin route
    path("", include("apps.authentication.urls")), # Auth routes - login / register

    # ADD NEW Routes HERE
    path("", include("apps.clients.urls")),     # client routes
    # path("", include("apps.orders.urls")),      # orders routes
    # path("", include("apps.products.urls")),    # product routes

    # Leave `Home.Urls` as last the last line
    path("", include("apps.home.urls"))
]
