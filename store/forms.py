from decimal import Decimal

from django import forms
from django.core.exceptions import ValidationError, ObjectDoesNotExist

from .models import Store


def validate_name(value):
    if isinstance(value, str):
        if len(value) > 10:
            raise ValidationError("Название слишком длинное")
    else:
        raise ValidationError("Название не должно содержать цифры, только буквы")


def validate_price(value):
    if not isinstance(value, Decimal):
        raise ValidationError("Поле должно содержать только цифры")


def validate_description(value):
    if len(value) > 10:
        raise ValidationError("Описание слишком длинное")

VALID_IMAGE_EXTENSIONS = [
    ".jpg",
    ".jpeg",
    ".png",
    ".gif",
]
def validate_image(value):
    naming, ext = value.split(".")
    print(naming)
    print(ext)
    if ext not in VALID_IMAGE_EXTENSIONS:
        raise ValidationError('Не валидный формат файла')


def validate_store(value):
    try:
        Store.objects.get(id=value)
    except ObjectDoesNotExist:
        raise ValidationError("Магазин не существует!")



class AddProductForms(forms.Form):
    name = forms.CharField(max_length=50, label='Название', validators=[validate_name],)
    price = forms.DecimalField(max_digits=6, decimal_places=2, label='Цена', validators=[validate_price],)
    description = forms.CharField(required=False, label='Описание', widget=forms.Textarea,validators=[validate_description],)
    image = forms.ImageField(required=False, label='Фотография', validators=[validate_image],)
    store = forms.ModelChoiceField(queryset=Store.objects.all(), label='Магазин', validators=[],)


