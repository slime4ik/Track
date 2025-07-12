from django.contrib import admin
from track.models import (
    Track,
    TrackComment,
    TrackImage,
    TrackCommentImage,
    TrackCategory
)

admin.site.register(Track)
admin.site.register(TrackComment)
admin.site.register(TrackCategory)
admin.site.register(TrackCommentImage)
admin.site.register(TrackImage)