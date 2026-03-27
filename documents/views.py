from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from documents.services import JinjaEmailService


class TestEmailAPIView(APIView):
    """ Тестовый API‑эндпоинт для проверки отправки HTML‑писем.

        Назначение:
        - создаёт экземпляр JinjaEmailService;
        - рендерит шаблон test.jinja;
        - отправляет письмо на указанный email;
        - возвращает JSON‑ответ об успешной отправке.

        Особенности:
        - доступен только авторизованным пользователям (IsAuthenticated);
        - метод GET перенаправляет на POST для удобства тестирования;
        - используется для проверки корректности шаблонов, SMTP‑настроек и сервиса отправки.
        """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return self.post(request)

    def post(self, request):
        """создаёт сервис-рендерит шаблон test.jinja-отправляет письмо-возвращает JSON‑ответ,"""
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