# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from apps.orders.models import Order
from datetime import datetime
import pytz

@login_required(login_url="/login/")
def index(request):
    context = {'segment': 'index'}

    get_today_info(context)
    
    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def pages(request):
    context = {}
    
    try:
        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template
        
        if load_template == 'index.html':
            get_today_info(context)


        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:
        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))


def get_today_info(context):
    today = datetime.now(pytz.timezone('Europe/Moscow')).date()
    today_info = Order._get_data_for_period(today, today)

    if len(today_info) == 0:
        return None

    context['today_revenue'] = today_info[0]['revenue']
    context['today_profit'] = today_info[0]['profit']
    context['today_orders'] = today_info[0]['orders_count']