from django.urls import path
from track.views import TrackListAPIView, TrackAnswersAPIView, \
    AnswerCommentAPIView, HomePageAPIView, TrackAPIView, ToggleTrackLikeAPIView


urlpatterns = [
    path('tracks/', TrackListAPIView.as_view(), name='tracks'),
    path('track/<uuid:track_id>/', TrackAPIView.as_view(), name='track_detail'),
    path('answers/<uuid:track_id>/', TrackAnswersAPIView.as_view(), name='track_answers'),
    path('comments/<uuid:answer_id>/', AnswerCommentAPIView.as_view(), name='answer_comments'),
    path('home/', HomePageAPIView.as_view(), name='home'),
    path('tracks/<uuid:track_id>/like/', ToggleTrackLikeAPIView.as_view(), name='track-like-toggle'),
]