from django.db import models
from django.conf import settings


class ProfileUser(models.Model):
    """
        Профиль пользователя, расширяющий кастомную модель User.

        Назначение:
        - хранит дополнительные данные, которые не входят в основную модель User;
        - обеспечивает хранение аватарки пользователя;
        - связан с User через отношение OneToOne, что гарантирует:
            * один пользователь → один профиль,
            * удобный доступ: user.profileuser и profile.user_profile.

        Поля:
        - user_profile — связь с кастомной моделью User. При удалении пользователя
          профиль удаляется автоматически (CASCADE).
        - image — аватарка пользователя. Хранится в MEDIA_ROOT/img/.
          Поле необязательное (null=True, blank=True).

        Использование:
        - создаётся автоматически при первом обращении (get_or_create в API);
        - используется в HTML‑профиле и API‑эндпоинтах для отображения и обновления аватарки.
        """

    user_profile = models.OneToOneField(settings.AUTH_USER_MODEL,  # Ссылается на кастомную модель User
        on_delete=models.CASCADE,
        verbose_name='Профиль пользователя')
    image = models.ImageField(upload_to='img', null=True, blank=True, verbose_name='Аватарка пользователя')

    def __str__(self):
        """Возвращает удобное строковое представление профиля."""
        return f"Профиль: {self.user_profile.email}"
