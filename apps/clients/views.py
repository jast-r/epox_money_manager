from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, QueryDict
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django.views import View
from django.shortcuts import render

from apps.clients.forms import ClientForm
from apps.clients.models import Client
from apps.utils import form_validation_error

def Clients(request):
    clients = Client.objects.all()
    context = {
        'segment': 'clients',
        'clients': clients,
    }

    return render(request, 'clients/clients.html', context)


@method_decorator(login_required(login_url='login'), name='dispatch')
class ClientView(View):
    context = {}

    def get(self, request, pk=None, action=None):
        if request.is_ajax():
            self.context['template'] = self.get_create_form(pk)

        return JsonResponse(self.context)

    def post(self, request, pk=None, action=None):
        form = ClientForm(request.POST)
        if form.is_valid():
            client = form.save()
            item = render_to_string('clients/row_item.html', {'client': client})

            response = {'valid': 'success', 'message': 'новый клиент создан успешно.', 'item': item}
        else:
            response = {'valid': 'error', 'message': form_validation_error(form)}
        return JsonResponse(response)

    def put(self, request, pk=None, action=None):
        client = self.get_object(pk)
        form = ClientForm(QueryDict(request.body), instance=client)
        if form.is_valid():
            client = form.save()
            item = render_to_string('clients/row_item.html', {'client': client})

            response = {'valid': 'success', 'message': 'client updated successfully.', 'item': item}
        else:
            response = {'valid': 'error', 'message': form_validation_error(form)}

        return JsonResponse(response)

    def get_create_form(self, pk=None):
        form = ClientForm()
        if pk:
            form = ClientForm(instance=self.get_object(pk))
        return render_to_string('clients/modal_form.html', {'form': form})

    def get_object(self, pk):
        client = Client.objects.get(id=pk)
        return client