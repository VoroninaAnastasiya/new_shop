import json

from rest_framework.renderers import  JSONRenderer


class UserJSONRenderer(JSONRenderer):
    """Кастомный рендерер, который приводит все ответы, связанные с пользователем,
    к единому формату и обеспечивает корректную сериализацию токенов.

    Назначение:
    - стандартизировать структуру всех JSON‑ответов вида:
          { "user": { ... } }
      Это делает API предсказуемым и удобным для фронтенда.

    - корректно обрабатывать токены, которые могут быть в формате bytes.
      Байтовые строки не сериализуются в JSON, поэтому рендерер
      декодирует их в UTF‑8."""

    charset = 'utf-8'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        """
                Преобразует данные перед сериализацией в JSON.

                Параметры:
                - data — словарь, который сериализатор передал во view.
                - accepted_media_type — тип контента (обычно application/json).
                - renderer_context — контекст рендеринга (request, response и т.д.).

                Логика:
                - если в ответе есть errors → вернуть стандартный JSON;
                - если token в формате bytes → декодировать в строку;
                - вернуть JSON в формате {"user": data}.
                """

        # Если мы получим ключ token как часть ответа, это будет байтовый
        # объект. Байтовые объекты плохо сериализуются, поэтому нам нужно
        # декодировать их перед рендерингом объекта User.
        token = data.get('token', None)
        errors = data.get('errors', None)

        if errors is not None:
            # Позволим стандартному JSONRenderer обрабатывать ошибку.
            return super(UserJSONRenderer, self).render(data)

        if token is not None and isinstance(token, bytes):
            #декодирует token если он имеет тип bytes.
            data['token'] = token.decode('utf-8')

        #отобразить наши данные в простанстве имен 'user'
        return json.dumps({
            'user': data
        })
