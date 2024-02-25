from django import forms

from .models import Store


class AddProductForms(forms.Form):
    name = forms.CharField(max_length=50, label='Название')
    price = forms.DecimalField(max_digits=6, decimal_places=2, label='Цена')
    descriptions = forms.DurationField(required=False, label='Описание', widget=forms.Textarea)
    image = forms.ImageField(required=False, label='Фотография')
    store = forms.ModelChoiceField(queryset=Store.objects.all(), label='Магазин')