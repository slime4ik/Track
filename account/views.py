from django.core.cache import cache
from django.contrib.auth import authenticate
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from drf_spectacular.utils import extend_schema
import uuid

from account.serializers import (
    UsernameEmailSerializer, EmailCodeSerializer,
    PasswordSerializer, UsernamePasswordSerializer
)
from account.models import User
from account.utils import set_code_in_redis, check_code_in_redis
from account.tasks import send_code_to_email


# Регистрация — email
class RegistrationEmailAPIView(GenericAPIView):
    serializer_class = UsernameEmailSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            username = serializer.validated_data['username']
            code = set_code_in_redis(email)

            reg_token = str(uuid.uuid4())
            cache.set(f'reg:{reg_token}', {'email': email, 'username': username}, timeout=900)

            send_code_to_email.delay(email, code)
            return Response({'message': 'Код отправлен на почту', 'reg_token': reg_token})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Регистрация — код
class RegistrationCodeAPIView(GenericAPIView):
    serializer_class = EmailCodeSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            reg_token = request.data.get('reg_token')
            if not reg_token:
                return Response({'message': 'Нужен токен регистрации'}, status=status.HTTP_403_FORBIDDEN)

            reg_data = cache.get(f'reg:{reg_token}')
            if not reg_data:
                return Response({'message': 'Истёк токен регистрации'}, status=status.HTTP_403_FORBIDDEN)

            if not check_code_in_redis(reg_data['email'], serializer.validated_data['code']):
                return Response({'message': 'Неверный код'}, status=status.HTTP_403_FORBIDDEN)

            cache.set(f'reg:{reg_token}', {**reg_data, 'code_verified': True}, timeout=1800)
            return Response({'message': 'Код принят, придумайте пароль!', 'reg_token': reg_token})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Регистрация — пароль
class RegistrationPasswordAPIView(GenericAPIView):
    serializer_class = PasswordSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            reg_token = request.data.get('reg_token')
            reg_data = cache.get(f'reg:{reg_token}')

            if not reg_data or not reg_data.get('code_verified'):
                return Response({'message': 'Регистрация не подтверждена'}, status=status.HTTP_403_FORBIDDEN)

            user = User.objects.create(username=reg_data['username'], email=reg_data['email'])
            user.set_password(serializer.validated_data['password'])
            user.save()
            cache.delete(f'reg:{reg_token}')

            refresh = RefreshToken.for_user(user)
            response = Response({
                'message': 'Аккаунт создан!',
                'access': str(refresh.access_token)
            }, status=status.HTTP_201_CREATED)

            response.set_cookie(
                key='refresh_token',
                value=str(refresh),
                httponly=True,
                secure=True,
                samesite='Lax',
                max_age=7 * 24 * 3600
            )
            return response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Вход — логин + пароль
class LoginAPIView(GenericAPIView):
    serializer_class = UsernamePasswordSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(
                username=serializer.validated_data['username'],
                password=serializer.validated_data['password']
            )
            if not user:
                return Response({'message': 'Неверный логин или пароль'}, status=status.HTTP_403_FORBIDDEN)

            login_token = str(uuid.uuid4())
            code = set_code_in_redis(user.email)
            cache.set(f'login:{login_token}', user.email, timeout=300)

            send_code_to_email.delay(user.email, code)
            return Response({'message': 'Код отправлен на почту', 'login_token': login_token})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Вход — код
class LoginCodeAPIView(GenericAPIView):
    serializer_class = EmailCodeSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            login_token = request.data.get('login_token')
            email = cache.get(f'login:{login_token}')
            if not login_token or not email:
                return Response({'message': 'Истёк токен или не указан'}, status=status.HTTP_403_FORBIDDEN)

            if not check_code_in_redis(email, serializer.validated_data['code']):
                return Response({'message': 'Неверный код'}, status=status.HTTP_403_FORBIDDEN)

            user = User.objects.get(email=email)
            refresh = RefreshToken.for_user(user)
            cache.delete(f'login:{login_token}')

            response = Response({
                'message': 'Успешный вход!',
                'access': str(refresh.access_token)
            }, status=status.HTTP_200_OK)

            response.set_cookie(
                key='refresh_token',
                value=str(refresh),
                httponly=True,
                secure=True,
                samesite='Lax',
                max_age=7 * 24 * 3600
            )
            return response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Logout
class LogoutAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.COOKIES.get('refresh_token')
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
            response = Response({'message': 'Вы вышли из аккаунта'}, status=status.HTTP_205_RESET_CONTENT)
            response.delete_cookie('refresh_token')
            return response
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)


# Проверка авторизации
class CheckAuthAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({
            'message': 'Вы авторизованы!',
            'user_id': request.user.id,
            'username': request.user.username
        })