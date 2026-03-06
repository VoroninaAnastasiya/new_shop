from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from documents.services import JinjaEmailService


class TestEmailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return self.post(request)

    def post(self, request):
        service = JinjaEmailService(
            template_name='test.jinja',
            context={
                'user': request.user,
                'order': None,
            },
            to_email='voronina-nastya.97@yandex.ru'
        )

        service.send('Тестовое письмо')

        return Response({"message": "Письмо отправлено!"})


from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse


# def test_email(request):#TODO переделать  на drf, post, is auth,
#     send_mail(
#         'Тестовое письмо',
#         'Поздравляем! Ваш заказ оформлен',
#         settings.EMAIL_HOST_USER,
#         ['voronina-nastya.97@yandex.ru'],
#         fail_silently=False,
#     )
#     return HttpResponse("Письмо отправлено!") # старое








