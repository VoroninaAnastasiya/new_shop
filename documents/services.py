from django.template.loader import select_template
from django.core.mail import EmailMessage
from django.conf import settings


class JinjaEmailService:
    """ Сервис для рендера и отправки HTML‑писем на основе Jinja‑шаблонов.

        Назначение:
        - рендерит Jinja‑шаблон в готовый HTML‑текст письма;
        - формирует EmailMessage с HTML‑контентом;
        - отправляет письмо на указанный email;
        - поддерживает прикрепление файлов.

        Параметры:
        - template_name — имя Jinja‑шаблона (например, 'emails/order_success.jinja');
        - context — словарь данных, которые будут подставлены в шаблон;
        - to_email — адрес получателя;
        - file_path — путь к файлу, который нужно прикрепить (опционально).

        Методы:
        - render():
            Загружает шаблон через select_template и рендерит его с переданным контекстом.
            Возвращает HTML‑строку.
        - send(subject):
            Создаёт EmailMessage, подставляет HTML‑тело письма,
            устанавливает content_subtype='html', прикрепляет файл (если есть)
            и отправляет письмо.

        Особенности:
        - select_template позволяет гибко искать шаблон по нескольким путям;
        - content_subtype='html' гарантирует корректное отображение HTML‑письма;
        - сервис изолирует логику отправки писем, что улучшает архитектуру проекта.
        """
    def __init__(self, template_name, context, to_email, file_path=None):
        self.template_name = template_name
        self.context = context
        self.to_email = to_email
        self.file_path = file_path

    def render(self):
        template = select_template([self.template_name]) #select_template ищет шаблон по имени
        return template.render(self.context)#превращает Jinja‑шаблон в готовый HTML

    def send(self, subject):
        '''метод создаёт EmailMessage,подставляет HTML‑тело письма,
        устанавливает content_subtype='html', чтобы письмо отображалось как HTML.'''
        email = EmailMessage(
            subject=subject,
            body=self.render(),
            from_email=settings.EMAIL_HOST_USER,
            to=[self.to_email],
        )
        email.content_subtype = 'html'

        if self.file_path:
            email.attach_file(self.file_path)

        email.send(fail_silently=False)