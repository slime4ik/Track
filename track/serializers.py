from rest_framework import serializers
from track.models import (
    Track,
    TrackComment,
    TrackImage,
    TrackCommentImage,
    TrackCategory
)
class TrackImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrackImage
        fields = ['image']

class TrackSerializer(serializers.ModelSerializer):
    # Для записи (принимаем IDs категорий)
    category_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=TrackCategory.objects.all(),
        source='category',  # связь с полем модели
        write_only=True,
        required=False
    )
    # Для чтения (показываем названия)
    category = serializers.SerializerMethodField(read_only=True)
    likes = serializers.SerializerMethodField()
    total_likes = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(format='%d-%m-%Y %H:%M', read_only=True)
    edited_at = serializers.DateTimeField(format='%d-%m-%Y %H:%M', read_only=True)
    images = TrackImageSerializer(many=True, read_only=False, required=False)
    completed = serializers.BooleanField(read_only=True)

    class Meta:
        model = Track
        fields = (
            'creator',
            'created_at',
            'edited_at',
            'subject',
            'description',
            'category_ids',  # для записи
            'category',      # для чтения
            'privacy',
            'completed',
            'likes',
            'total_likes',
            'images'
        )

    def get_category(self, obj):
        return [category.name for category in obj.category.all()]

    def get_likes(self, obj):
        return [user.username for user in obj.likes.all()]

    def get_total_likes(self, obj):
        return obj.likes.count()
