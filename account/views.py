import uuid
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.cache import cache
from account.serializers import (
    UsernameEmailSerializer, EmailCodeSerializer,
    PasswordSerializer, UsernamePasswordSerializer
)
from account.models import User
from account.utils import set_code_in_redis, check_code_in_redis
from account.tasks import send_code_to_email
from drf_spectacular.utils import extend_schema


@extend_schema(
    request=UsernameEmailSerializer,
    responses={200: None, 400: UsernameEmailSerializer}
)
class RegistrationEmailAPIView(GenericAPIView):
    serializer_class = UsernameEmailSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            username = serializer.validated_data['username']
            code = set_code_in_redis(email)
            
            # Генерируем временный токен для регистрации
            reg_token = str(uuid.uuid4())
            cache.set(f'reg:{reg_token}', {'email': email, 'username': username}, timeout=900)  # 15 минут
            
            send_code_to_email.delay(email, code)
            return Response({
                'message': 'Код отправлен на почту',
                'reg_token': reg_token
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    request=EmailCodeSerializer,
    responses={200: None, 400: EmailCodeSerializer}
)
class RegistrationCodeAPIView(GenericAPIView):
    serializer_class = EmailCodeSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            code = serializer.validated_data['code']
            reg_token = request.data.get('reg_token')
            
            if not reg_token:
                return Response({'message': 'Требуется начать регистрацию заново'}, status=status.HTTP_403_FORBIDDEN)
                
            reg_data = cache.get(f'reg:{reg_token}')
            if not reg_data:
                return Response({'message': 'Время регистрации истекло'}, status=status.HTTP_403_FORBIDDEN)
            
            email = reg_data['email']
            if check_code_in_redis(email, code):
                # Обновляем данные в кеше
                cache.set(f'reg:{reg_token}', {**reg_data, 'code_verified': True}, timeout=1800)
                return Response({
                    'message': 'Теперь придумайте пароль!',
                    'reg_token': reg_token
                }, status=status.HTTP_200_OK)
            return Response({'message': 'Неверный код'}, status=status.HTTP_403_FORBIDDEN)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    request=PasswordSerializer,
    responses={201: None, 400: PasswordSerializer}
)
class RegistrationPasswordAPIView(GenericAPIView):
    serializer_class = PasswordSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            reg_token = request.data.get('reg_token')
            
            if not reg_token:
                return Response({'message': 'Требуется начать регистрацию заново'}, status=status.HTTP_403_FORBIDDEN)
                
            reg_data = cache.get(f'reg:{reg_token}')
            if not reg_data or not reg_data.get('code_verified'):
                return Response({'message': 'Время регистрации истекло или код не подтвержден'}, 
                              status=status.HTTP_403_FORBIDDEN)
            
            email = reg_data['email']
            username = reg_data['username']
            password = serializer.validated_data['password']
            
            user = User.objects.create(username=username, email=email)
            user.set_password(password)
            user.save()
            
            # Очищаем временные данные
            cache.delete(f'reg:{reg_token}')
            
            refresh = RefreshToken.for_user(user)
            return Response({
                'message': 'Аккаунт успешно создан!',
                'access': str(refresh.access_token),
                'refresh': str(refresh),
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    request=UsernamePasswordSerializer,
    responses={200: None, 400: UsernamePasswordSerializer}
)
class LoginAPIView(GenericAPIView):
    serializer_class = UsernamePasswordSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(username=username, password=password)
            
            if not user:
                return Response({'message': 'Неверный логин или пароль'}, status=status.HTTP_403_FORBIDDEN)
            
            # Генерируем временный токен для входа
            login_token = str(uuid.uuid4())
            code = set_code_in_redis(user.email)
            
            # Сохраняем email пользователя по токену
            cache.set(f'login:{login_token}', user.email, timeout=300)  # 5 минут
            
            send_code_to_email.delay(user.email, code)
            return Response({
                'message': 'Код отправлен вам на почту',
                'login_token': login_token
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    request=EmailCodeSerializer,
    responses={200: None, 400: EmailCodeSerializer}
)
class LoginCodeAPIView(GenericAPIView):
    serializer_class = EmailCodeSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            code = serializer.validated_data['code']
            login_token = request.data.get('login_token')
            
            if not login_token:
                return Response({'message': 'Требуется выполнить вход заново'}, status=status.HTTP_403_FORBIDDEN)
            
            email = cache.get(f'login:{login_token}')
            if not email:
                return Response({'message': 'Время действия кода истекло'}, status=status.HTTP_403_FORBIDDEN)
            
            if not check_code_in_redis(email, code):
                return Response({'message': 'Неверный код'}, status=status.HTTP_403_FORBIDDEN)
            
            user = User.objects.get(email=email)
            refresh = RefreshToken.for_user(user)
            
            # Очищаем временные данные
            cache.delete(f'login:{login_token}')
            
            return Response({
                'message': 'Вы успешно вошли в аккаунт!',
                'access': str(refresh.access_token),
                'refresh': str(refresh),
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    request=None,
    responses={205: None, 400: None}
)
class LogoutAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    request=None,
    responses={200: None}
)
class CheckAuthAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({
            'message': 'Вы авторизованы!',
            'user_id': request.user.id,
            'username': request.user.username
        })