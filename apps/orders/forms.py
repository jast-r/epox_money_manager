from django import forms
from apps.orders.models import Order
from apps.clients.models import Client
from apps.products.models import Product

class OrderForm(forms.ModelForm):
    client_tg = forms.CharField(
        label="Ник в тг",
        widget=forms.TextInput(attrs={
            'class': 'form-control order',
            'autocomplete': ''
        })
    )
    client_phone = forms.CharField(
        label="Номер телефона",
        widget=forms.TextInput(attrs={
            'class': 'form-control order',
            'autocomplete': ''
        })
    )
    client_fio = forms.CharField(
        label="ФИО",
        widget=forms.TextInput(attrs={
            'class': 'form-control order',
            'autocomplete': ''
        })
    )
    product = forms.ModelChoiceField(
        label="Наименование",
        widget=forms.Select(attrs={
            'class': 'form-select order',
            'autocomplete': ''
        }),
        empty_label=None,
        queryset=Product.objects.all()
    )
    quantity = forms.IntegerField(
        label="Количество",
        widget=forms.NumberInput(attrs={
            'class': 'form-control order',
            'inputmode': 'numeric',
            'min': '1',
            'type': 'text',
            'autocomplete': ''
        })
    )
    sell_price = forms.IntegerField(
        label="Цена",
        widget=forms.NumberInput(attrs={
            'class': 'form-control order',
            'inputmode': 'numeric',
            'min': '1',
            'type': 'text',
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
        fields = [
            'product',
            'client_fio',
            'client_tg',
            'client_phone',
            'quantity', 
            'sell_price', 
            'address', 
            'description', 
            'priority',
        ]

    # Переопределяем отображаемое значение для поля client и product
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['product'].label_from_instance = lambda obj: obj.name