from django.shortcuts import render

from django.core.mail import send_mail
from django.http import HttpResponse

from django.core.mail import send_mail
from django.http import HttpResponse
from django.conf import settings

def test_email(request):#TODO переделать  на drf, post, is auth,
    send_mail(
        'Тестовое письмо',
        'Поздравляем! Ваш заказ оформлен',
        settings.EMAIL_HOST_USER,
        ['voronina-nastya.97@yandex.ru'],
        fail_silently=False,
    )
    return HttpResponse("Письмо отправлено!")
