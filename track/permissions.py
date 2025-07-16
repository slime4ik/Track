from rest_framework.permissions import BasePermission
from track.models import Track

class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Проверяем, что пользователь - создатель трека
        return obj.creator == request.user
