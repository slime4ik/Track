from django.urls import path
from track.api_views import TrackListAPIView


urlpatterns = [
    path('tracks/', TrackListAPIView.as_view(), name='tracks')
]
