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
    price = forms.FloatField(
        label="Себестоимость",
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
        }),
        required=False,
    )

    class Meta:
        model = Product
        fields = ['name', 'type', 'price']
