from django.shortcuts import render
from rest_framework import generics
from track.serializers import TrackSerializer
from rest_framework.permissions import (
    IsAuthenticated,
    IsAdminUser,
    AllowAny,
)
from track.models import (
    Track,
    TrackComment,
    TrackImage,
    TrackCommentImage,
    TrackCategory
)
# Create your views here.
class TrackListAPIView(generics.ListCreateAPIView):
    queryset = Track.objects.\
        select_related('creator').\
        prefetch_related('category', 'images').all()
    serializer_class = TrackSerializer
    permission_classes = [IsAuthenticated]