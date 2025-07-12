from django.urls import path
from track.views import track_list, track_create

app_name = 'track'

urlpatterns = [
    path('tracks/', track_list, name='track_list'),
    path('track/create/', track_create, name='create'),
]
