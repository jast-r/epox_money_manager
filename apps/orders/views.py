from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, QueryDict
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django.views import View
from django.shortcuts import render

from apps.orders.forms import OrderForm
from apps.orders.models import Order
from apps.utils import form_validation_error

def Orders(request):
    orders = Order.objects.filter(deleted_at=None).order_by('-id').all()
    context = {
        'segment': 'orders',
        'orders': orders,
    }

    return render(request, 'orders/orders.html', context)


def DeleteOrder(request, pk):
    Order.objects.filter(pk=pk).delete()

    context = {
        'segment': 'orders',
    }

    return render(request, 'orders/orders.html', context)


@method_decorator(login_required(login_url='login'), name='dispatch')
class OrderView(View):
    context = {}

    def get(self, request, pk=None, action=None):
        if request.is_ajax():
            self.context['template'] = self.get_create_form(pk)

        return JsonResponse(self.context)

    def post(self, request, pk=None, action=None):
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save()
            item = render_to_string('orders/row_item.html', {'order': order})

            response = {'valid': 'success', 'message': 'Новый заказ создан успешно.', 'item': item}
        else:
            response = {'valid': 'error', 'message': form_validation_error(form)}

        return JsonResponse(response)

    def put(self, request, pk=None, action=None):
        order = self.get_object(pk)
        form = OrderForm(QueryDict(request.body), instance=order)
        if form.is_valid():
            order = form.save()
            item = render_to_string('orders/row_item.html', {'order': order})

            response = {'valid': 'success', 'message': 'Заказ обновлен успешно.', 'item': item}
        else:
            response = {'valid': 'error', 'message': form_validation_error(form)}

        return JsonResponse(response)

    def delete(self, request, pk=None, action=None):
        Order.objects.filter(pk=pk).update(deleted_at=timezone.now())
        response = {'valid': 'success', 'message': 'Заказ удален успешно.'}
        return JsonResponse(response)

    def get_create_form(self, pk=None):
        form = OrderForm()
        if pk:
            form = OrderForm(instance=self.get_object(pk))
        return render_to_string('orders/modal_form.html', {'form': form})

    def get_object(self, pk):
        order = Order.objects.get(id=pk)
        return order