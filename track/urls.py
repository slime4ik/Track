from django.urls import path
from track.views import track_list

app_name = 'track'

urlpatterns = [
    path('tracks/', track_list, name='track_list')
]
