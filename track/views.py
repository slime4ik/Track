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
from rest_framework import status
from rest_framework.response import Response
# Кастомные фильтры
from track.filters import PublicTracksFilterBackend, TracksFilterBackend
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from django.shortcuts import render
from rest_framework import generics
# Кастомные permissions
from track.permissions import IsOwner
# Серилизаторы
from track.serializers import TrackSerializer, TrackAnswerSerializer, \
    AnswerCommentSerializer, HomePageSerializer, TrackDetailSerializer
# Пагинация
from track.pagination import TrackListPagination, AnswerListPagination, AnswerCommentPagination
from rest_framework.pagination import PageNumberPagination
from django.db.models import Prefetch, F
from account.models import User
from django.conf import settings
from django.core.cache import cache
from rest_framework.views import APIView

# Апи для отображения публичных треков и создания своих
class TrackListAPIView(generics.ListCreateAPIView):
    queryset = Track.objects.select_related('creator').prefetch_related(
        Prefetch('category', queryset=TrackCategory.objects.only('name', 'id')),
        Prefetch('images', queryset=TrackImage.objects.only('image', 'track_id'))).order_by('-created_at')
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
    
class TrackAPIView(generics.RetrieveDestroyAPIView):
    serializer_class = TrackDetailSerializer
    lookup_url_kwarg = 'track_id'

    def get_queryset(self):
        if self.request.method == 'DELETE':
            # Только creator — больше ничего не нужно
            return Track.objects.only('id', 'creator_id').select_related('creator')
        
        # Для GET — загружаем всё нужное для сериализатора
        return Track.objects.select_related('creator').prefetch_related(
            Prefetch('category', queryset=TrackCategory.objects.only('name', 'id')),
            Prefetch('images', queryset=TrackImage.objects.only('image', 'track_id'))
        ).annotate(
            creator_name=F('creator__username')
        )

    def get_permissions(self):
        self.permission_classes = [AllowAny]
        if self.request.method == 'DELETE':
            self.permission_classes = [IsOwner]
        return super().get_permissions()

class ToggleTrackLikeAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = None
    
    def post(self, request, track_id):
        user_id = request.user.id
        liked_users_key = f"track:{track_id}:liked_users"
        total_likes_key = f"track:{track_id}:likes"

        liked_users = set(cache.get(liked_users_key, []))

        if user_id in liked_users:
            liked_users.remove(user_id)
            cache.set(liked_users_key, list(liked_users))
            cache.decr(total_likes_key)
            liked = False
        else:
            liked_users.add(user_id)
            cache.set(liked_users_key, list(liked_users))
            if cache.get(total_likes_key) is None:
                cache.set(total_likes_key, 1)
            else:
                cache.incr(total_likes_key)
            liked = True

        total_likes = cache.get(total_likes_key, 0)

        return Response({
            "liked": liked,
            "total_likes": total_likes
        }, status=status.HTTP_200_OK)