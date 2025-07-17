from django.db import models
from uuid import uuid4
from django.conf import settings


class BaseCreateClass(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, 
                               on_delete=models.CASCADE,
                               related_name='%(class)s_created')
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True,
                                     blank=True,
                                     null=True)
    class Meta:
        abstract = True

class TrackCategory(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Track(BaseCreateClass):
    class Privacy(models.TextChoices):
        PUBLIC = 'PB', 'Публичный'
        PRIVATE = 'PR', 'Приватный'
    subject = models.CharField(max_length=300)
    description = models.CharField(max_length=3000)
    category = models.ManyToManyField(TrackCategory,
                                 related_name='tracks')
    privacy = models.CharField(max_length=2,
                               choices=Privacy.choices,
                               default=Privacy.PUBLIC)
    completed = models.BooleanField(default=False, blank=True)

    def __str__(self):
        return self.subject
    
class TrackImage(models.Model):
    track = models.ForeignKey(Track,
                              on_delete=models.CASCADE,
                              related_name='images')
    image = models.ImageField(upload_to='track_images/%Y/%m/%d/')

class TrackAnswer(BaseCreateClass):
    track = models.ManyToManyField(Track,
                                   related_name='answers')
    comment = models.CharField(max_length=2000)
    solution = models.BooleanField(default=False, blank=True)
    is_active = models.BooleanField(default=True,
                                    blank=True)
    def __str__(self):
        return self.comment[:20]

class TrackAnswerImage(models.Model):
    answer = models.ForeignKey(TrackAnswer,
                              on_delete=models.CASCADE,
                              related_name='images')
    image = models.ImageField(upload_to='track_comment_images/%Y/%m/%d/')

class AnswerComment(BaseCreateClass):
    answer = models.ForeignKey(TrackAnswer,
                               on_delete=models.CASCADE,
                               related_name='comments')
    comment = models.CharField(max_length=500)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.comment[:20]