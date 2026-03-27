from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User


class  RegistrationSerializer(serializers.ModelSerializer):
    """ Сериализатор для регистрации нового пользователя.

    Сериализация регистрации пользователя и создания нового.
    Принимает email, username, password, name, lastname, phone,
    валидирует их согласно правилам модели и DRF.
    Вызывает User.objects.create_user() и возвращает созданного пользователя.

    Особенности:
    - поле password write_only=True — пароль не возвращается клиенту;
    - минимальная длина пароля — 8 символов;
    - сериализатор возвращает объект пользователя, но не токены
      (токены создаются во view через RefreshToken.for_user())."""


    # пароль содержит не менее 8 символов, не более 128,
    # и так же он не может быть прочитан клиентской стороной
    password = serializers.CharField(max_length=128, min_length=8,write_only=True)
    # Клиент не должен иметь возможность отправлять токен вместе с
    # запросом на регистрацию. Сделаем его доступным только на чтение.


    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'name', 'lastname', 'contact_phone')

    def create(self, validated_data):
        '''Создаёт нового пользователя через кастомный менеджер UserManager.'''
        # Используем метод create_user, который мы написали ранее, для создания нового пользователя.
        return User.objects.create_user(**validated_data)


class UserSerializer(serializers.ModelSerializer):
    """ Сериализатор для чтения и обновления данных пользователя.

    Назначение:
    - сериализует профиль пользователя (email, username, имя, телефон и т.д.);
    - позволяет частично обновлять данные (используется с partial=True);
    - при обновлении пароля вызывает set_password(), чтобы пароль
      был захэширован, а не сохранён в открытом виде.

    - password write_only=True — пароль не возвращается клиенту;
    - token read_only=True — поле оставлено для совместимости,
    но фактически токены создаются через SimpleJWT во view."""

    token = serializers.CharField(max_length=128, min_length=8, read_only=True)
    password = serializers.CharField(max_length=128, min_length=8, write_only=True)
    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'name', 'lastname', 'contact_phone', 'token', 'password') #в примере без токена

    def update(self, instance, validated_data):
        """ Выполняет обновление User.
        Логика:
        - извлекает пароль, если он передан;
        - обновляет остальные поля через setattr();
        - если пароль передан — хэширует его через set_password();
        - сохраняет изменения.

        Возвращает обновлённый объект User."""

        password = validated_data.pop('password', None)

        for key, value in validated_data.items():
            setattr(instance, key, value) #Для ключей, оставшихся в validated_data мы устанавливаем значения
        # в текущий экземпляр User по одному.

        if password is not None:
            instance.set_password(password) # 'set_password()' - встроенный механизм Django для безопасного
            # хэширования паролей. Он не сохраняет пароль в открытом виде, set_password() не сохраняет модель.
            instance.save()

        return instance


class LoginSerializer(serializers.Serializer):
    """Сериализатор для аутентификации пользователя и выдачи JWT‑токенов.

        Назначение:
        - принимает email и пароль;
        - проверяет корректность данных;
        - вызывает authenticate(), который использует кастомный USERNAME_FIELD=email;
        - проверяет, что пользователь активен;
        - создаёт пару токенов (refresh + access) через SimpleJWT;
        - возвращает email, username и токены.

        Особенности:
        - username read_only=True — клиент не передаёт его при логине;
        - password write_only=True — пароль не возвращается клиенту;
        - access и refresh read_only=True — сериализатор сам их формирует.
        """

    email = serializers.CharField(max_length=255)
    username = serializers.CharField(max_length=255, read_only=True)
    password = serializers.CharField(max_length=100, write_only=True)
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)

    def validate(self, data):
        '''Проверяет корректность логина и создаёт JWT‑токены.
        Логика:
        - убеждается, что email и password переданы;
        - вызывает authenticate(email, password);
        - проверяет, что пользователь существует и активен;
        - создаёт refresh и access токены через RefreshToken.for_user();
        - возвращает словарь данных, который попадёт в Response.

        Возвращает:
        {
            'email': user.email,
            'username': user.username,
            'access': <access_token>,
            'refresh': <refresh_token>
        }'''

        # В методе validate мы убеждаемся, что текущий экземпляр
        # LoginSerializer значение valid. В случае входа пользователя в систему
        # это означает подтверждение того, что присутствуют адрес электронной
        # почты и то, что эта комбинация соответствует одному из пользователей.
        email = data.get('email', None)
        password = data.get('password', None)

        # Вызвать исключение, если не предоставлена почта
        if email is None:
            raise serializers.ValidationError('An email address is required to log in')

        # Вызвать исключение, если не предоставлен пароль
        if password is None:
           raise serializers.ValidationError('A password is required to log in')

        # Метод authenticate предоставляется Django и выполняет проверку, что
        # предоставленные почта и пароль соответствуют какому-то пользователю в
        # нашей базе данных. Мы передаем email как username, так как в модели
        # пользователя USERNAME_FIELD = email.

        user = authenticate(username=email, password=password)

        # Если пользователь с данными почтой/паролем не найден, то authenticate
        # вернет None. Возбудить исключение в таком случае.
        if user is None:
            raise serializers.ValidationError('Invalid credentials')

        # флаг is_active для модели User - сообщает, был ли пользователь деактивирован или заблокирован.
        # Проверить стоит, вызвать исключение в случае True.
        if not user.is_active:
            raise serializers.ValidationError('This user has been deactivated.')

        refresh = RefreshToken.for_user(user)

        # Метод validate должен возвращать словать проверенных данных. Это
        # данные, которые передются в т.ч. в методы create и update.
        return {
            'email': user.email,
            'username': user.username,
            'access': str(refresh.access_token),
            'refresh': str(refresh)
        }