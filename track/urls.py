from django.urls import path
from track.views import TrackListAPIView


urlpatterns = [
    path('tracks/', TrackListAPIView.as_view(), name='tracks')
]