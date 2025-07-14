from rest_framework.permissions import (
    IsAuthenticated,
    IsAdminUser,
    AllowAny,
    IsAuthenticatedOrReadOnly,
)
from track.models import (
    Track,
    TrackComment,
    TrackImage,
    TrackCommentImage,
    TrackCategory
)
# Кастомные фильтры
from track.filters import PublicTracksFilterBackend, TracksFilterBackend
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from django.shortcuts import render
from rest_framework import generics
# Серилизаторы
from track.serializers import TrackSerializer 
# Пагинация
from track.pagination import TrackListPagination
from rest_framework.pagination import PageNumberPagination

# Апи для отображения публичных треков и создания своих
class TrackListAPIView(generics.ListCreateAPIView):
    queryset = Track.objects.\
        select_related('creator').\
        prefetch_related('category',
                         'images',
                         'likes').all()
    serializer_class = TrackSerializer
    permission_classes = [IsAuthenticatedOrReadOnly] # Разрешаем всем get, а post авторизированым
    filter_backends = [
        PublicTracksFilterBackend,  # твой кастомный фильтр
        DjangoFilterBackend,         # для TracksFilter
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_class = TracksFilterBackend
    search_fields = ['subject', 'description'] # /?search=emazing для точного поиска =subject или =description в ''
    ordering_fields = ['created_at', 'likes']  # /?search=-likes
    # ======== PAGINATION ========
    pagination_class = TrackListPagination # Используем кастомный пагинатор
    # ======== PAGINATION ========