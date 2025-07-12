from rest_framework import serializers
from track.models import (
    Track,
    TrackComment,
    TrackImage,
    TrackCommentImage,
    TrackCategory
)

class TrackSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField()
    total_likes = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(format='%d-%m-%Y %H:%M')
    class Meta:
        model = Track
        fields = (
            'creator',
            'created_at',
            'edited_at',
            'subject',
            'description',
            'category',
            'privacy',
            'completed',
            'likes',
            'total_likes'
        )

    def get_likes(self, obj):
        return [user.username for user in obj.likes.all()]

    def get_total_likes(self, obj):
        return obj.likes.count()
