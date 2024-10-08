from datetime import timedelta

from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, QueryDict
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django.views import View
from django.shortcuts import render, get_object_or_404

from apps.orders.forms import OrderForm
from apps.orders.models import Order
from apps.utils import form_validation_error

def Orders(request):
    """View для отображения всех заказов"""
    orders = Order.objects.filter(deleted_at=None).order_by('-id').all()

    # Форматирование данных для отображения
    for order in orders:
        order.client_fio = order.client_fio.replace(' ', '\n')
        parts = [part.strip() for part in order.address.split(',')]
        if len(parts) >= 2:
            order.address = ', '.join(parts[:2]) + '\n' + ', '.join(parts[2:])
        else:
            order.address = order.address

    context = {
        'segment': 'orders',
        'orders': orders,
    }

    return render(request, 'orders/orders.html', context)


def DeleteOrder(request, pk):
    """View для удаления заказа"""
    Order.objects.filter(pk=pk).update(deleted_at=timezone.now())  # Обновляем поле deleted_at вместо физического удаления

    context = {
        'segment': 'orders',
    }

    return render(request, 'orders/orders.html', context)


def get_total_info(request):
    period = request.GET.get('period', 'week')
    total_info = Order._get_data_for_period(period)

    result = []

    for item in total_info:
        result.append({
            "date": item['created_at'].strftime("%d.%m.%Y"),
            "revenue": item.get('revenue') or 0,
            "profit": item.get('profit') or 0,
        })

    return JsonResponse({'data': result})
    
@method_decorator(login_required(login_url='login'), name='dispatch')
class OrderView(View):
    """Класс для обработки CRUD операций с заказами и расчета прибыли/выручки"""
    context = {}

    def get(self, request, pk=None, action=None):
        if request.is_ajax():
            self.context['template'] = self.get_create_form(pk)

        return JsonResponse(self.context, safe=False)

    def post(self, request, pk=None, action=None):
        """Метод POST: Создает новый заказ"""
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save()
            # Возвращаем новый заказ в виде HTML элемента для обновления страницы
            item = render_to_string('orders/row_item.html', {'order': order})
            response = {'valid': 'success', 'message': 'Новый заказ создан успешно.', 'item': item}
        else:
            response = {'valid': 'error', 'message': form_validation_error(form)}
        return JsonResponse(response)

    def put(self, request, pk=None, action=None):
        """Метод PUT: Обновляет существующий заказ"""
        order = self.get_object(pk)
        form = OrderForm(QueryDict(request.body), instance=order)
        if form.is_valid():
            order = form.save()
            # Возвращаем обновленный заказ в виде HTML элемента для обновления страницы
            item = render_to_string('orders/row_item.html', {'order': order})
            response = {'valid': 'success', 'message': 'Заказ обновлен успешно.', 'item': item}
        else:
            response = {'valid': 'error', 'message': form_validation_error(form)}
        return JsonResponse(response)

    def delete(self, request, pk=None, action=None):
        """Метод DELETE: Помечает заказ как удаленный (soft delete)"""
        Order.objects.filter(pk=pk).update(deleted_at=timezone.now())
        response = {'valid': 'success', 'message': 'Заказ удален успешно.'}
        return JsonResponse(response)

    def get_create_form(self, pk=None):
        """Возвращает HTML с формой для создания или редактирования заказа"""
        form = OrderForm()
        if pk:
            form = OrderForm(instance=self.get_object(pk))  # Если pk передан, заполняем форму данными заказа
        return render_to_string('orders/modal_form.html', {'form': form})

    def get_object(self, pk):
        """Получает объект заказа по его первичному ключу (pk)"""
        return get_object_or_404(Order, pk=pk)
    