from idlelib.rpc import request_queue
from logging import raiseExceptions

from django.shortcuts import redirect
from rest_framework.generics import RetrieveUpdateAPIView
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.core.serializers import serialize
from rest_framework import status, generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import RegistrationSerializer, UserSerializer, LoginSerializer
from .renderers import UserJSONRenderer


class LoginHTMLView(APIView):
    '''Проверяет данные и возвращает токены.'''
    renderer_classes = [TemplateHTMLRenderer]
    permission_classes = [AllowAny]
    template_name = 'login.html'

    def get(self, request):
        return Response({})

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, email=email, password=password)
        if user:
            login(request, user)
            next_url = (
                request.GET.get('next')
                or request.POST.get('next')
                or 'home_page'
            )
            return redirect(next_url)

        return Response(
            {'error': "Введены неверные логин или пароль"},
            template_name='login.html'
        )



class LogoutHTMLView(APIView):
    '''вызывает logout() и редиректит на главную.'''
    permission_classes = [IsAuthenticated]

    def get(self, request):
        logout(request)
        return redirect('home_page')


class RegistrationHTMLView(APIView):
    '''логинит пользователя, проверяет, что email уникален, вызывает create_user '''
    renderer_classes = [TemplateHTMLRenderer]
    permission_classes = [AllowAny]
    template_name = 'register.html'

    def get(self, request):
        return Response({})

    def post(self, request):
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')

        if User.objects.filter(email=email).exists():
            return Response({'error': 'Email уже используется'},template_name='register.html')

        user = User.objects.create_user(
            email=email,
            username=username,
            password=password
        )

        login(request, user)
        return redirect('home_page')


class RegistrationAPIView(APIView):
    """
    Разрешить всем пользователям (аутентифицированным и нет) доступ к данному эндпоинту.
    """
    permission_classes = (AllowAny,)  # кто может использовать
    serializer_class = RegistrationSerializer
    renderer_classes = (UserJSONRenderer,)

    def post(self, request):
        # Паттерн создания сериализатора, валидации и сохранения - стандартный
        serializer = self.serializer_class(data=request.data.get('user', {}))
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        refresh = RefreshToken.for_user(user) #создаёт пару токенов для конкретного пользователя

        return Response({
            "user": {
                "id": user.id,
                "email": user.email,
                "username": user.username,
                "access": str(refresh.access_token),
                "refresh": str(refresh)
            }
        }, status=status.HTTP_201_CREATED)


User = get_user_model() #метод возвращает именно ту модель User, которая указана в AUTH_USER_MODEL.


class UserListAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ProfileAPIView(APIView):
    """
        API‑профиль текущего пользователя.
        GET — возвращает данные пользователя.
        PUT — частично обновляет профиль (partial=True).

        Использует RegistrationSerializer, так как он содержит нужные поля.
        """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Возвращает данные текущего пользователя."""
        user = request.user
        serializer = RegistrationSerializer(user)
        return Response(serializer.data)

    def put(self, request):
        """Частично обновляет профиль пользователя.
            partial=True позволяет обновлять только переданные поля."""
        user = request.user
        serializer = RegistrationSerializer(user, data=request.data,
                                                  partial=True) #Обнови только поля, которые пришли в запросе.
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(APIView):
    """
        API‑логин пользователя с выдачей JWT‑токенов.
        - принимает JSON {"user": {"email": ..., "password": ...}};
        - LoginSerializer.validate() проверяет данные и создаёт токены;
        - возвращает access и refresh токены.

        В отличие от HTML‑логина, здесь не используется Django‑сессия.
        """
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = LoginSerializer

    def post(self, request):
        """Проверяет данные и возвращает JWT‑токены."""
        user = request.data.get('user', {})  # мы не вызываем метод save() сериализатора, как
        # делали это для регистрации. в данном случае нам нечего сохранять.
        # Вместо этого, метод validate() делает все нужное.
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    """
        API‑эндпоинт для получения и обновления данных текущего пользователя.
        GET — возвращает профиль.
        PUT/PATCH — частично обновляет данные (partial=True).
        Использует UserJSONRenderer для единообразного формата ответа.
        """
    permission_classes = (IsAuthenticated,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = UserSerializer

    def retrieve(self, request, *args, **kwargs):
        """Возвращает данные текущего пользователя."""
        # сериализатор обрабатывал преобразования объекта User во что-то, что
        # можно привести к json и вернуть клиенту.
        serializer = self.serializer_class(request.user)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        """Частично обновляет данные пользователя.
           partial=True позволяет обновлять только переданные поля."""
        serializer_data = request.data.get('user', {})
        # Паттерн сериализации, валидирования и сохранения
        serializer = self.serializer_class(
            request.user, data=serializer_data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer_data, status=status.HTTP_200_OK)


class LogoutAPIView(APIView):
    '''API‑логаут для JWT‑авторизации. обрабатывает запросы на выход из системы (логаут).
    - принимает refresh‑токен;
    - помещает его в blacklist;
    - access‑токен автоматически становится недействительным после истечения срока.

    Используется только при JWT‑авторизации.'''
    permission_classes = [IsAuthenticated]

    def post(self,request):
        """Добавляет refresh‑токен в blacklist и завершает сессию JWT."""
        refresh_token = request.data.get('refresh')

        if not refresh_token: #проверка, что токен вообще передан.
            return Response({"error": "Refresh token is required"},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            token = RefreshToken(refresh_token)#создание объекта RefreshToken из строки.
            token.blacklist()#добавляем токен в «чёрный список», blacklist помечает токен как недействительный.
            return Response({"detail": "Вы успешно вышли из системы."}, status=status.HTTP_205_RESET_CONTENT)
            #HTTP_205_RESET_CONTENT означает, что клиенту стоит «сбросить» своё состояние. Например, на фронте.
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


