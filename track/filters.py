import django_filters
from track.models import Track
from rest_framework import filters
from django_filters import rest_framework

# Для отображения публичных треков
class PublicTracksFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        return queryset.filter(privacy=Track.Privacy.PUBLIC)

class TracksFilterBackend(django_filters.FilterSet):  # Используем django_filters.FilterSet
    category = django_filters.CharFilter(  # Используем django_filters.CharFilter
        field_name="category__name",
        lookup_expr="iexact",
    )
    
    class Meta:
        model = Track
        fields = {
            'id': ['exact'],
            'subject': ['iexact', 'icontains'],
            'description': ['iexact', 'icontains'],
            'category': ['exact']
        }