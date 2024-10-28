from datetime import datetime, timedelta, date

from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, QueryDict
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django.views import View
from django.shortcuts import render, get_object_or_404

from apps.orders.forms import OrderForm
from apps.orders.models import Order
from apps.utils import form_validation_error, set_pagination

def Orders(request):
    context = {
        'segment': 'orders',
    }

    orders = Order.objects.filter(deleted_at=None).order_by('-id').all()

    # Форматирование данных для отображения
    for order in orders:
        order.client_fio = order.client_fio.replace(' ', '\n')
        parts = [part.strip() for part in order.address.split(',')]
        if len(parts) >= 2:
            order.address = ', '.join(parts[:2]) + '\n' + ', '.join(parts[2:])
        else:
            order.address = order.address

    context['orders'], context['info'] = set_pagination(request, orders, item_numer=10)

    return render(request, 'orders/orders.html', context)


def DeleteOrder(request, pk):
    """View для удаления заказа"""
    Order.objects.filter(pk=pk).update(deleted_at=timezone.now())  # Обновляем поле deleted_at вместо физического удаления

    context = {
        'segment': 'orders',
    }

    return render(request, 'orders/orders.html', context)


def get_total_info(request):
    """View для получения общей информации о прибыли и выручке за период"""
    start_date = datetime.strptime(request.GET.get('start_date'), "%Y-%m-%d").date()
    end_date = datetime.strptime(request.GET.get('end_date'), "%Y-%m-%d").date()

    total_info = TotalInfoCalculator.get_total_info(start_date, end_date)

    if (360 <= (end_date - start_date).days <= 370):
        total_info = TotalInfoCalculator.get_monthly_summary(total_info)

    period_revenue = sum(item['revenue'] for item in total_info)
    period_profit = sum(item['profit'] for item in total_info)
    period_orders = sum(item['orders_count'] for item in total_info)
    period_customers = sum(item['customers_count'] for item in total_info)

    return JsonResponse(
        {
            'data': total_info,
            'period_revenue': period_revenue,
            'period_profit': period_profit,
            'period_orders': period_orders,
            'period_customers': period_customers
        }
    )


def update_order_status(request, order_id):
    try:
        order = Order.objects.get(id=order_id)
        new_status = request.POST.get('status')

        if new_status:
            order.status = new_status
            order.save()
            return JsonResponse({'valid': 'success', 'message': 'Статус заказа обновлен.'})
        else:
            return JsonResponse({'valid': 'error', 'message': 'Статус не указан.'})
    except Order.DoesNotExist:
        return JsonResponse({'valid': 'error', 'message': 'Заказ не найден.'})


class TotalInfoCalculator:
    month_names = {
        1: "Янв.",
        2: "Фев.",
        3: "Март",
        4: "Апр.",
        5: "Май",
        6: "Июнь",
        7: "Июль",
        8: "Авг.",
        9: "Сен.",
        10: "Окт.",
        11: "Нояб.",
        12: "Дек.",
    }

    @staticmethod
    def get_total_info(start_date, end_date):
        """Получение общей информации о прибыли и выручке за период"""
        if not start_date or not end_date:
            return []
        
        total_info = Order._get_data_for_period(start_date, end_date)
        result = TotalInfoCalculator.format_result(total_info)
        result = TotalInfoCalculator.fill_missing_dates(result, start_date, end_date)

        return result

    @staticmethod
    def format_result(total_info):
        result = []
        for item in total_info:
            result.append({
                "date": item['created_at_date'],
                "revenue": item['revenue'],
                "profit": item['profit'],
                "customers_count": item['customers_count'],
                "orders_count": item['orders_count']
            })

        return result

    @staticmethod
    def fill_missing_dates(result, start_date, end_date):
        """Заполнение отсутствующих дат"""
        if not result:
            return result

        filled_result = []
        current_date = start_date

        for item in result:
            while current_date < item['date']:
                filled_result.append({
                    "date": current_date,
                    "revenue": 0,
                    "profit": 0,
                    "customers_count": 0,
                    "orders_count": 0
                })
                current_date += timedelta(days=1)
            
            filled_result.append(item)
            current_date = item['date'] + timedelta(days=1)

        while current_date <= end_date:
            filled_result.append({
                "date": current_date,
                "revenue": 0,
                "profit": 0,
                "customers_count": 0,
                "orders_count": 0
            })
            current_date += timedelta(days=1)

        return filled_result

    @staticmethod
    def get_monthly_summary(data):
        monthly_summary = {}
        
        for item in data:
            month = item['date'].month
            month_name = TotalInfoCalculator.month_names[month]

            if month_name not in monthly_summary:
                monthly_summary[month_name] = {"revenue": 0, "profit": 0, "customers_count": 0, "orders_count": 0}

            monthly_summary[month_name]['revenue'] += item['revenue']
            monthly_summary[month_name]['profit'] += item['profit']
            monthly_summary[month_name]['customers_count'] += item['customers_count']
            monthly_summary[month_name]['orders_count'] += item['orders_count']
        monthly_summary = [
            {
                "month": month,
                "revenue": data['revenue'],
                "profit": data['profit'],
                "customers_count": data['customers_count'],
                "orders_count": data['orders_count']
            }
            for month, data in monthly_summary.items()
        ]

        return monthly_summary


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
    