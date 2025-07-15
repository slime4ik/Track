from rest_framework.permissions import (
    IsAuthenticated,
    IsAdminUser,
    AllowAny,
    IsAuthenticatedOrReadOnly,

)
from track.models import (
    Track,
    TrackAnswer,
    TrackImage,
    TrackAnswerImage,
    TrackCategory,
    AnswerComment
)
from rest_framework.response import Response
# Кастомные фильтры
from track.filters import PublicTracksFilterBackend, TracksFilterBackend
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from django.shortcuts import render
from rest_framework import generics
# Серилизаторы
from track.serializers import TrackSerializer, TrackAnswerSerializer, AnswerCommentSerializer, HomePageSerializer
# Пагинация
from track.pagination import TrackListPagination, AnswerListPagination, AnswerCommentPagination
from rest_framework.pagination import PageNumberPagination
from django.db.models import Prefetch, Count
from django.contrib.postgres.aggregates import ArrayAgg
from account.models import User
from django.conf import settings
from django.core.cache import cache

# Апи для отображения публичных треков и создания своих
class TrackListAPIView(generics.ListCreateAPIView):
    queryset = (
        Track.objects
        .annotate(
            total_likes_count=Count('likes'),
            category_names=ArrayAgg('category__name', distinct=True),
        )
        .select_related('creator')
        .prefetch_related(
            Prefetch('images', queryset=TrackImage.objects.only('track_id', 'image')),
        )
    )
    serializer_class = TrackSerializer
    permission_classes = [IsAuthenticatedOrReadOnly] # Разрешаем всем get, а post авторизированым
    filterset_class = TracksFilterBackend
    filter_backends = [
        PublicTracksFilterBackend,  # кастомный фильтр
        DjangoFilterBackend,         # для TracksFilter
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    search_fields = ['=id', 'subject', 'description', 'category__name'] # /?search=emazing для точного поиска =subject или =description в ''
    ordering_fields = ['created_at', 'likes']  # /?search=-likes
    # ======== PAGINATION ========
    pagination_class = TrackListPagination # Используем кастомный пагинатор
    # ======== PAGINATION ========

class TrackAnswersAPIView(generics.ListAPIView):
    pagination_class = AnswerListPagination
    serializer_class = TrackAnswerSerializer

    # Достаем track_id из urla
    def get_queryset(self):
        track_id = self.kwargs['track_id']
        return TrackAnswer.objects.filter(
            track__id=track_id
        ).select_related('creator').prefetch_related('images')

class AnswerCommentAPIView(generics.ListCreateAPIView):
    queryset = AnswerComment.objects.\
                            select_related('creator', 'answer').\
                            only('created_at', 'edited_at', 'comment', 'creator__username')
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = AnswerCommentSerializer
    # Пагинация кастомная
    pagination_class = AnswerCommentPagination
    # Достаем track_id из urla
    def get_queryset(self):
        answer_id = self.kwargs['answer_id']
        return AnswerComment.objects.filter(
            answer__id=answer_id
        ).select_related('creator')


class HomePageAPIView(generics.GenericAPIView):
    """
    Вьюха для главной страницы с агрегированными данными
    """
    serializer_class = HomePageSerializer

    def get(self, request, *args, **kwargs):
        # Подготавливаем данные для сериализации
        total_tracks = cache.get('total_tracks')
        context = {
            'categories': TrackCategory.objects.all(),
            'total_tracks': total_tracks
        }
        
        # Добавляем дополнительные данные в контекст
        context.update(self.get_extra_context())
        
        serializer = self.get_serializer(context)
        return Response(serializer.data)

    def get_extra_context(self):
        """
        Метод для добавления дополнительных данных
        Переопределите в дочерних классах или добавьте нужные поля
        """
        return {}