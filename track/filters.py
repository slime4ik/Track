import django_filters
from track.models import Track
from rest_framework import filters

# Для отображения публичных треков
class PublicTracksFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        return queryset.filter(privacy=Track.Privacy.PUBLIC)

class TracksFilterBackend(django_filters.FilterSet):
    class Meta:
        model = Track
        fields = {
            'subject': ['iexact', 'icontains'],
            'description': ['iexact', 'icontains'],
        }