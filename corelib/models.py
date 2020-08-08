from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class VideoLib(models.Model):
    title = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Video(models.Model):
    title = models.CharField(max_length=255)
    url = models.URLField()
    youtube_id = models.CharField(max_length=255)
    videolib = models.ForeignKey(VideoLib, on_delete=models.CASCADE)
