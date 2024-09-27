from django import forms
from apps.products.models import Product

class ProductForm(forms.ModelForm):
    name = forms.CharField(
        label="Наименование",
        widget=forms.TextInput(attrs={
            'class': 'form-control product',
            'autocomplete': ''  
        })
    )
    description = forms.CharField(
        label="Описание продукта",
        widget=forms.TextInput(attrs={
            'class': 'form-control product',
            'autocomplete': ''  
        })
    )
    price = forms.FloatField(
        label="Цена",
        widget=forms.TextInput(attrs={
            'class': 'form-control product',
            'autocomplete': ''  
        })
    )
    type = forms.CharField(
        label="Тип",
        widget=forms.TextInput(attrs={
            'class': 'form-control product',
            'autocomplete': ''  
        })
    )

    class Meta:
        model = Product
        fields = ['name', 'description', 'type', 'price']
