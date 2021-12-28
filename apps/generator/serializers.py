from rest_framework import serializers
from typing_extensions import Required

from .models import Album, AlbumUserHistory


class AlbumSerializer(serializers.ModelSerializer):

    class Meta:

        model = Album

        fields = (
            "id",
            "album_position",
            "album_artist",
            "album_name",
            "album_label",
            "album_year",
            "album_critic",
            "album_genre",
            "album_subgenre",
        )


class AlbumUserHistorySerializer(serializers.ModelSerializer):

    album_generated = AlbumSerializer(read_only=True)

    class Meta:

        model = AlbumUserHistory

        fields = (
            "id",
            "generated_order",
            "user_ranked_order",
            "album_generated",
        )
