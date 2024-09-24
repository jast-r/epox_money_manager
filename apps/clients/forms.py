from django import forms

from clients.models import Client


class ClientForm(forms.ModelForm):
    tg_username = forms.CharField(label="Ник в телеграмм", widget=forms.TextInput(attrs={'class': 'form-control client'}))
    phone = forms.CharField(label="Номер телефона", widget=forms.TextInput(attrs={'class': 'form-control client'}))

    class Meta:
        model = Client
        fields = ['tg_username', 'phone']
