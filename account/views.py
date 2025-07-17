from rest_framework.views import APIView
from account.serializers import UsernameEmailSerializer, EmailCodeSerializer,\
PasswordSerializer, UsernamePasswordSerializer
from account.models import User
from rest_framework.response import Response
from rest_framework import status
from account.utils import *
from account.tasks import send_code_to_email
# JWT
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
# RATE LIMIT
from django_ratelimit.decorators import ratelimit
from django_ratelimit.exceptions import Ratelimited

class RegistrationEmailAPIView(APIView):
    @ratelimit(key='ip', rate='5/m', block=True)
    def post(self, request):
        serializer = UsernameEmailSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            username = serializer.validated_data['username']
            code = set_code_in_redis(email)
            send_code_to_email(email, code)
            request.session['email'] = email
            request.session['registration_username'] = username
            return Response({'message': 'Код отправлен на почту'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RegistrationCodeAPIView(APIView):
    @ratelimit(key='ip', rate='3/10m', block=True)
    def post(self, request):
        serializer = EmailCodeSerializer(data=request.data)
        if serializer.is_valid():
            code = serializer.validated_data['code']
            email = request.session.get('email', False)
            if not email:
                return Response({'message': 'Для начала введите вашу почту'}, status=status.HTTP_403_FORBIDDEN)
            if check_code_in_redis(email, code):
                request.session['code'] = code
                return Response({'message': 'Теперь придумайте себе ник!'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class RegistrationPasswordAPIView(APIView):
    @ratelimit(key='ip', rate='5/m', block=True)
    def post(self, request):
        serializer = PasswordSerializer(data=request.data)
        if serializer.is_valid():
            username = request.session.get('registration_username')
            email = request.session.get('email')
            password = serializer.validated_data['password']
            if not (username and email):
                return Response({'messages': 'Произошла ошибка, попробуйте пройти регистрацию сначала'}, status=status.HTTP_403_FORBIDDEN)
            user = User.objects.create(username=username, email=email)
            user.set_password(password)
            user.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'message': 'Аккаунт успешно создан!',
                'access': str(refresh.access_token),
                'refresh': str(refresh),
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginAPIView(APIView):
    @ratelimit(key='ip', rate='5/m', block=True)
    def post(self, request):
        serializer = UsernamePasswordSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(username=username, password=password)
            if not user:
                return Response({'messages': 'Неверный логин или пароль'}, status=status.HTTP_403_FORBIDDEN)
            request.session['email'] = user.email
            code = set_code_in_redis(user.email)
            send_code_to_email(user.email, code)
            return Response({'messages': 'Код отправлен вам на почту'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginCodeAPIView(APIView):
    @ratelimit(key='ip', rate='3/10m', block=True)
    def post(self, request):
        serializer = EmailCodeSerializer(data=request.data)
        if serializer.is_valid():
            code = serializer.validated_data['code']
            email = request.session.get('email')
            if not email:
                return Response({'message': 'Ошибка, попробуйте выполнить вход заново'}, status=status.HTTP_403_FORBIDDEN)
            if not check_code_in_redis(email, code):
                return Response({'message': 'Неверный код'}, status=status.HTTP_403_FORBIDDEN)
            user = User.objects.get(email=email)
            if not user:
                return Response({'message': 'Такого пользователя не существует'}, status=status.HTTP_403_FORBIDDEN)
            refresh = RefreshToken.for_user(user)
            return Response({
                'message': 'Вы успешно вошли в аккаунт!',
                'access': str(refresh.access_token),
                'refresh': str(refresh),
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutAPIView(APIView):
    @ratelimit(key='ip', rate='7/m', block=True)
    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class CheckAuthAPIView(APIView):
    permission_classes = [IsAuthenticated]
    @ratelimit(key='ip', rate='5/m', block=True)
    def get(self, request):
        return Response({'message': 'Вы авторизованы!'})