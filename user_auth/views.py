from logging import raiseExceptions
from rest_framework.generics import RetrieveUpdateAPIView
from django.contrib.auth import get_user_model
from django.core.serializers import serialize
from rest_framework import status, generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import RegistrationSerializer, UserSerializer, LoginSerializer
from .renderers import UserJSONRenderer


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

        refresh = RefreshToken.for_user(user)

        return Response({
            "user": {
                "id": user.id,
                "email": user.email,
                "username": user.username,
                "access": str(refresh.access_token),
                "refresh": str(refresh)
            }
        }, status=status.HTTP_201_CREATED)


User = get_user_model()


class UserListAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated] #нужно скрыть, чтобы не все могли видеть список всех наших пользователей, только админ
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = RegistrationSerializer(user)
        return Response(serializer.data)

    def put(self, request):
        user = request.user
        serializer = RegistrationSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(APIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = LoginSerializer

    def post(self, request):
        user = request.data.get('user', {})  # мы не вызываем метод save() сериализатора, как
        # делали это для регистрации. в данном случае нам нечего сохранять.
        # Вместо этого, метод validate() делает все нужное.
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = UserSerializer

    def retrieve(self, request, *args, **kwargs):
        # сериализатор обрабатывал преобразования объекта User во что-то, что
        # можно привести к json и вернуть клиенту.
        serializer = self.serializer_class(request.user)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        serializer_data = request.data.get('user', {})
        # Паттерн сериализации, валидирования и сохранения
        serializer = self.serializer_class(
            request.user, data=serializer_data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer_data, status=status.HTTP_200_OK)


class LogoutAPIView(APIView):
    '''API‑эндпоинт, который обрабатывает запросы на выход из системы (логаут).'''
    permission_classes = [IsAuthenticated]

    def post(self,request):
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


