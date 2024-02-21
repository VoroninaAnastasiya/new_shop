from django import forms

from store.models import Store


class AddProductForms(forms.Form):
    name = forms.CharField(max_length= 50)
    price = forms.DecimalField(max_digits=6, decimal_places=2)
    store = forms.ModelChoiceField(queryset=Store.objects.all())