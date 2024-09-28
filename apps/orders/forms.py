from django import forms
from apps.orders.models import Order

class OrderForm(forms.ModelForm):
    client = forms.ModelChoiceField(
        label="Клиент",
        widget=forms.Select(attrs={
            'class': 'form-control order',
            'autocomplete': ''
        }),
        queryset=Order.objects.none(),
    )
    product = forms.ModelChoiceField(
        label="Продукт",
        widget=forms.Select(attrs={
            'class': 'form-control order',
            'autocomplete': ''
        }),
        queryset=Order.objects.none(),
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
        choices=Order.PRIORITIES.items()
    )

    class Meta:
        model = Order
        fields = ['client', 'product', 'quantity', 'sell_price', 'address', 'description', 'priority']
