from rest_framework import serializers
from track.models import (
    Track,
    TrackAnswer,
    TrackImage,
    TrackAnswerImage,
    TrackCategory,
    AnswerComment,
)

class TrackImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrackImage
        fields = ['image']

class TrackSerializer(serializers.ModelSerializer):
    category_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=TrackCategory.objects.all(),
        source='category',  # связь с полем модели
        write_only=True,
        required=False
    )
    # Для чтения (показываем названия)
    category = serializers.SerializerMethodField(read_only=True)
    total_likes = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(format='%d-%m-%Y %H:%M', read_only=True)
    edited_at = serializers.DateTimeField(format='%d-%m-%Y %H:%M', read_only=True)
    images = TrackImageSerializer(many=True, read_only=False, required=False)
    completed = serializers.BooleanField(read_only=True)
    creator = serializers.SerializerMethodField()
    class Meta:
        model = Track
        fields = (
            'id',
            'creator',
            'created_at',
            'edited_at',
            'subject',
            'description',
            'category_ids',  # для записи
            'category',      # для чтения
            'privacy',
            'completed',
            'total_likes',
            'images'
        )
    
    # Валидация

    # Методы

    def get_category(self, obj):
        return [category.name for category in obj.category.all()]

    def get_creator(self, obj):
        return obj.creator.username

    def get_total_likes(self, obj):
        return obj.likes.count()

    def create(self, validated_data):
        # Автоматически подставляем текущего пользователя как создателя
        validated_data['creator'] = self.context['request'].user
        return super().create(validated_data)

class TrackAnswerImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrackAnswerImage
        fields = ['image']

class TrackAnswerSerializer(serializers.ModelSerializer):
    images = TrackAnswerImageSerializer(many=True, read_only=True)
    created_at = serializers.DateTimeField(format='%d-%m-%Y %H:%M', read_only=True)
    edited_at = serializers.DateTimeField(format='%d-%m-%Y %H:%M', read_only=True)
    creator = serializers.SerializerMethodField()
    class Meta:
        model = TrackAnswer
        fields = (
            'id',
            'creator',
            'comment',
            'solution',
            'images',
            'created_at',
            'edited_at',
        )

    def get_creator(self, obj):
        return obj.creator.username

class AnswerCommentSerializer(serializers.ModelSerializer):
    creator = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(format='%d-%m-%Y %H:%M', read_only=True)
    edited_at = serializers.DateTimeField(format='%d-%m-%Y %H:%M', read_only=True)
    id = serializers.UUIDField(read_only=True)

    class Meta:
        model = AnswerComment
        fields = ('creator', 'created_at', 'edited_at', 'comment', 'id')

    def get_creator(self, obj):
        return obj.creator.username

    def create(self, validated_data):
        # Получаем answer_id из URL
        answer_id = self.context['view'].kwargs['answer_id']
        # Устанавливаем текущего пользователя и ответ
        validated_data['creator'] = self.context['request'].user
        validated_data['answer'] = TrackAnswer.objects.get(id=answer_id)  # Привязываем к ответу
        
        return super().create(validated_data)

class TotalTracksSerializer(serializers.ModelSerializer):
    total_tracks = serializers.SerializerMethodField()
    
    class Meta:
        model = Track
        fields = ('total_tracks',)

    def get_total_tracks(self, obj):
        """
        Возвращает общее количество треков в системе
        """
        return Track.objects.count()

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TrackCategory
        fields = (
            'name',
        )

class HomePageSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True)
    total_tracks = TotalTracksSerializer(read_only=True)

    class Meta:
        model = TrackCategory
        fields = (
            'categories',
            'total_tracks'
        )

    def get_categories(self, obj):
        categories = TrackCategory.objects.all()
        return [{'name': category.name} for category in categories]

    def get_total_tracks(self, obj):
        """
        Возвращает общее количество треков в системе
        """
        return Track.objects.count()

class TrackDetailSerializer(serializers.ModelSerializer):
    images = TrackImageSerializer(many=True, read_only=False, required=False)
    category = serializers.SerializerMethodField()
    is_owner = serializers.SerializerMethodField()
    creator = serializers.CharField()
    created_at = serializers.DateTimeField(format='%d-%m-%Y %H:%M', read_only=True)
    edited_at = serializers.DateTimeField(format='%d-%m-%Y %H:%M', read_only=True)

    class Meta:
        model = Track
        fields = (
            'creator',
            'subject',
            'description',
            'created_at',
            'edited_at',
            'category',
            'is_owner',
            'images'
        )

    def get_category(self, obj):
        return [c.name for c in obj.category.all()]

    def get_is_owner(self, obj):
        request = self.context.get('request')
        return request and request.user == obj.creator