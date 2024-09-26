from django import forms
from apps.clients.models import Client

class ClientForm(forms.ModelForm):
    name = forms.CharField(
        label="Имя",
        widget=forms.TextInput(attrs={
            'class': 'form-control client',
            'autocomplete': 'name'  # Атрибут для автозаполнения имени
        })
    )
    tg_username = forms.CharField(
        label="Ник в телеграмм",
        widget=forms.TextInput(attrs={
            'class': 'form-control client',
            'autocomplete': 'username'  # Атрибут для автозаполнения ника
        })
    )
    phone = forms.CharField(
        label="Номер телефона",
        widget=forms.TextInput(attrs={
            'class': 'form-control client',
            'autocomplete': 'tel'  # Атрибут для автозаполнения телефона
        })
    )

    class Meta:
        model = Client
        fields = ['name', 'tg_username', 'phone']
