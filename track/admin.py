from django.contrib import admin
from track.models import (
    Track,
    TrackAnswer,
    TrackImage,
    TrackAnswerImage,
    TrackCategory,
    AnswerComment
)

admin.site.register(Track)
admin.site.register(TrackAnswer)
admin.site.register(TrackCategory)
admin.site.register(TrackAnswerImage)
admin.site.register(TrackImage)
admin.site.register(AnswerComment)