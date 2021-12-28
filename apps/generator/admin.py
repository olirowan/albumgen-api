from django.contrib import admin
from .models import Album, AlbumUserHistory

admin.site.register(Album)
admin.site.register(AlbumUserHistory)
