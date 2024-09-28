from django import forms
from apps.orders.models import Order
from apps.clients.models import Client
from apps.products.models import Product

class OrderForm(forms.ModelForm):
    client = forms.ModelChoiceField(
        label="Клиент",
        widget=forms.Select(attrs={
            'class': 'form-control order',
            'autocomplete': ''
        }),
        empty_label=None,
        queryset=Client.objects.all()
    )
    product = forms.ModelChoiceField(
        label="Продукт",
        widget=forms.Select(attrs={
            'class': 'form-control order',
            'autocomplete': ''
        }),
        empty_label=None,
        queryset=Product.objects.all()
    )
    quantity = forms.IntegerField(
        label="Количество",
        widget=forms.NumberInput(attrs={
            'class': 'form-control order',
            'autocomplete': ''
        })
    )
    sell_price = forms.FloatField(
        label="Цена продажи",
        widget=forms.NumberInput(attrs={
            'class': 'form-control order',
            'autocomplete': ''
        })
    )
    address = forms.CharField(
        label="Адрес",
        widget=forms.TextInput(attrs={
            'class': 'form-control order',
            'autocomplete': ''
        })
    )
    description = forms.CharField(
        label="Описание",
        widget=forms.TextInput(attrs={
            'class': 'form-control order',
            'autocomplete': ''
        })
    )
    priority = forms.ChoiceField(
        label="Приоритет",
        widget=forms.Select(attrs={
            'class': 'form-control order',
            'autocomplete': ''
        }),
        choices=Order.Priority.choices
    )

    class Meta:
        model = Order
        fields = ['client', 'product', 'quantity', 'sell_price', 'address', 'description', 'priority']

    # Переопределяем отображаемое значение для поля client и product
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['client'].label_from_instance = lambda obj: obj.tg_username
        self.fields['product'].label_from_instance = lambda obj: obj.name