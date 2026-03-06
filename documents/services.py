from django.template.loader import select_template
from django.core.mail import EmailMessage
from django.conf import settings


class JinjaEmailService:
    def __init__(self, template_name, context, to_email, file_path=None):
        self.template_name = template_name
        self.context = context
        self.to_email = to_email
        self.file_path = file_path

    def render(self):
        template = select_template([self.template_name])
        return template.render(self.context)

    def send(self, subject):
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