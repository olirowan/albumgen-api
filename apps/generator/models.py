from django.contrib.auth.models import User
from django.db import models
from django.db.models.deletion import CASCADE


class Album(models.Model):

    album_position = models.IntegerField(blank=True, null=True)
    album_artist = models.CharField(max_length=255, blank=True, null=True)
    album_name = models.CharField(max_length=255, blank=True, null=True)
    album_label = models.CharField(max_length=255, blank=True, null=True)
    album_year = models.CharField(max_length=255, blank=True, null=True)
    album_critic = models.TextField(blank=True, null=True)
    album_genre = models.CharField(max_length=255, blank=True, null=True)
    album_subgenre = models.CharField(max_length=255, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)


class AlbumUserHistory(models.Model):

    user_generated = models.ForeignKey(
        User, related_name="generated_album", on_delete=models.CASCADE)
    album_generated = models.ForeignKey(
        Album, related_name="generated_by_user", on_delete=models.CASCADE)

    generated_order = models.IntegerField(default=0, blank=True, null=True)
    user_ranked_order = models.IntegerField(default=0, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
