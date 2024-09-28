from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, QueryDict
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django.views import View
from django.shortcuts import render

from apps.products.forms import ProductForm
from apps.products.models import Product
from apps.utils import form_validation_error

def Products(request):
    products = Product.objects.filter(deleted_at=None).order_by('id').all()
    context = {
        'segment': 'products',
        'products': products,
    }

    return render(request, 'products/products.html', context)


@method_decorator(login_required(login_url='login'), name='dispatch')
class ProductView(View):
    context = {}

    def get(self, request, pk=None, action=None):
        if request.is_ajax():
            self.context['template'] = self.get_create_form(pk)

        return JsonResponse(self.context)

    def post(self, request, pk=None, action=None):
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save()
            item = render_to_string('products/row_item.html', {'product': product})

            response = {'valid': 'success', 'message': 'новый продукт добавлен успешно.', 'item': item}
        else:
            response = {'valid': 'error', 'message': form_validation_error(form)}
        return JsonResponse(response)

    def put(self, request, pk=None, action=None):
        product = self.get_object(pk)
        form = ProductForm(QueryDict(request.body), instance=product)
        if form.is_valid():
            product = form.save()
            item = render_to_string('products/row_item.html', {'product': product})

            response = {'valid': 'success', 'message': 'Продукт обновлен успешно.', 'item': item}
        else:
            response = {'valid': 'error', 'message': form_validation_error(form)}

        return JsonResponse(response)

    def delete(self, request, pk=None, action=None):
        Product.objects.filter(pk=pk).update(deleted_at=timezone.now())
        response = {'valid': 'success', 'message': 'Продукт удален успешно.'}
        return JsonResponse(response)

    def get_create_form(self, pk=None):
        form = ProductForm()
        if pk:
            form = ProductForm(instance=self.get_object(pk))
        return render_to_string('products/modal_form.html', {'form': form})

    def get_object(self, pk):
        product = Product.objects.get(id=pk)
        return product