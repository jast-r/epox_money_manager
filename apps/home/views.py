# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from apps.clients.models import Client
from apps.orders.models import Order


@login_required(login_url="/login/")
def index(request):
    context = {'segment': 'index'}

    context['today_clients'] = Client.today_clients()
    context['today_orders'] = Order.today_orders()
    context['today_revenue'] = Order.today_revenue()
    context['today_profit'] = Order.today_profit()


    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:
        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template
        
        if load_template == 'index.html':
            context['today_clients'] = Client.today_clients()
            context['today_orders'] = Order.today_orders()
            context['today_revenue'] = Order.today_revenue()
            context['today_profit'] = Order.today_profit()


        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:
        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))
