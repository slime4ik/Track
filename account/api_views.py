from account.serializers import EmailPasswordSerializer, EmailCodeSerializer, UsernameSerializer
from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from account.models import User
from django.contrib.auth.hashers import make_password
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import make_password
from rest_framework import status
from account.utils import *
from account.tasks import *
# ВХОД
# 1.зашли
# 2.ввод почта, пароль
# 3.выполняется функция которая отправляет код
# 3.1. с этим рендерится страница с кодом async 
# 4. Вводим код, при успешном вводе кода получаем токен ура 

# РЕГИСТРАЦИЯ
# 1.почта, пароль
# 2.код вводим если верно делаем ник иначе повтори попытку
# 3.делаем токен

class UserRegistrationAPIView(generics.CreateAPIView):
    serializer_class = EmailPasswordSerializer
    def post(self, request):
        serializer = EmailPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Валидация прошла — сохраняем в сессию
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        hashed_password = make_password(password)
        request.session['email'] = email
        request.session['password'] = hashed_password
        request.session['step'] = 1
        # set in redis и отправляем
        code = set_code_in_redis(email)
        send_code_to_email.delay(email, code)

        return Response({'detail': f'Код {code} отправлен на почту {email}'}, status=status.HTTP_200_OK)

class UserCodeRegistrationAPIView(APIView):
    def post(self, request):
        step = request.session['step']
        if step != 1:
            return Response({'detail': 'Доступ запрещен'}, status=status.HTTP_403_FORBIDDEN)
        serializer = EmailCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        code = serializer.validate_date['code']
        email = request.session['email']
        if check_code_in_redis(email, code):
            request.session['step'] = 2
            return Response({'detail': 'Почта подтверждена!'}, status=status.HTTP_200_OK)
        
class UserUsernameRegistrationAPIView(APIView):
    def post(self, request):
        step = request.session['step']
        if step != 2:
            return Response({'detail': 'Доступ запрещен'}, status=status.HTTP_403_FORBIDDEN)
        serializer = UsernameSerializer
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        email = request.session['email']
        password = request.session['password']
        request.session.pop('email', None)
        request.session.pop('password', None)
        request.session.pop('step', None)
        try:
            User.objects.create(usename=username, email=email, password=password)
        except:
            return Response({'detail': 'Произошла ошибка при регистрации'}, status=status.HTTP_409_CONFLICT)
# class UserAuthAPIView(generics.CreateAPIView):
#     model = User
#     serializer_class = UserAuthSerializer

#     def post(self, request):
#         email = request.data.get("email")
#         code = request.data.get("code")

#         try:
#             user = User.objects.get(email=email)
#         except User.DoesNotExist:
#             raise AuthenticationFailed("Пользователь не найден")

#         if not user.profile.code or user.profile.code != code:
#             raise AuthenticationFailed("Неверный код")

#         # Если всё ок — выдаём токен
#         refresh = RefreshToken.for_user(user)
#         return Response({
#             'refresh': str(refresh),
#             'access': str(refresh.access_token)
#         })
