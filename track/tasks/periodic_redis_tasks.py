from django.core.cache import cache
from track.models import Track
from celery import shared_task

@shared_task
def set_total_tracks():
    tracks = Track.objects.count()
    cache.set('total_tracks', tracks, timeout=8000)