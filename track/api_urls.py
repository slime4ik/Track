from django.urls import path
from track.api_views import TrackListAPIView


urlpatterns = [
    path('tracks/', TrackListAPIView.as_view(), name='tracks')
]

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