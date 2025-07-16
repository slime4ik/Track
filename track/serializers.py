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
    category = serializers.CharField(source='category_names', read_only=True)
    category_ids = serializers.PrimaryKeyRelatedField(
        queryset=TrackCategory.objects.all(),
        many=True,
        write_only=True
    )
    created_at = serializers.DateTimeField(format='%d-%m-%Y %H:%M', read_only=True)
    edited_at = serializers.DateTimeField(format='%d-%m-%Y %H:%M', read_only=True)
    images = TrackImageSerializer(many=True, read_only=False, required=False)
    creator = serializers.CharField(source='creator.username', read_only=True)
    total_likes = serializers.IntegerField(source='total_likes_count', read_only=True)
    class Meta:
        model = Track
        fields = (
            'id',
            'creator',
            'created_at',
            'edited_at',
            'subject',
            'description',
            'category',       # read-only: список названий
            'category_ids',   # write-only: список id-шников
            'privacy',
            'completed',
            'total_likes',
            'images'
        )
    

    # Методы

    # def get_category(self, obj):
    #     # Используем аннотацию category_names
    #     return getattr(obj, 'category_names', [])
    
    # def get_images(self, obj):
    #     return [img.image.url for img in obj.images.all()]

    def create(self, validated_data):
        categories = validated_data.pop('category_ids', [])
        images_data = validated_data.pop('images', [])
        track = Track.objects.create(creator=self.context['request'].user, **validated_data)
        track.category.set(categories)

        for img_data in images_data:
            TrackImage.objects.create(track=track, **img_data)

        return track

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