from django.urls import path
from account.api_views import UserRegistrationAPIView, UserCodeRegistrationAPIView, UserUsernameRegistrationAPIView


urlpatterns = [
    path('sent_registration_code/', UserRegistrationAPIView.as_view(), name='registration_code'),
]