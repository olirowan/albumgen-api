import json
import logging
import random

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.decorators import (api_view)

from rest_framework import authentication, permissions
from rest_framework.decorators import api_view, authentication_classes, permission_classes

from .models import Album, AlbumUserHistory
from .serializers import AlbumSerializer, AlbumUserHistorySerializer

logger = logging.getLogger(__name__)


class AlbumViewSet(viewsets.ModelViewSet):

    serializer_class = AlbumSerializer

    queryset = Album.objects.all()

    def get_queryset(self):
        return self.queryset.filter()


@api_view(['GET'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def get_album(request):

    most_recent_album = AlbumUserHistory.objects.filter(
        user_generated=request.user.id).order_by('-created_at').first()

    album = get_object_or_404(
        Album, pk=most_recent_album.album_generated_id)

    serializer = AlbumSerializer(album)
    return JsonResponse(serializer.data, safe=False)


@api_view(['GET'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def generate_album(request):

    album_ids = Album.objects.filter().values('id')

    generated_album_ids = AlbumUserHistory.objects.filter(
        user_generated=request.user.id).values('album_generated_id')

    available_ids = set(album_ids.values_list('id', flat=True)).difference(list(generated_album_ids.values_list(
        'album_generated_id', flat=True)))

    if len(available_ids) >= 0:

        random_id = random.choice(list(available_ids))

        try:
            album = Album.objects.get(pk=random_id)

        except Album.DoesNotExist:

            album = None

    else:

        album = None

    try:
        most_recent_album = AlbumUserHistory.objects.filter(
            user_generated=request.user.id).order_by('-created_at').first()

    except Album.DoesNotExist:

        most_recent_album = None

    if most_recent_album is not None:

        album_generated_order = int(most_recent_album.generated_order) + 1
    else:

        album_generated_order = 1

    new_album_generated = AlbumUserHistory(
        album_generated=album,
        user_generated=request.user,
        generated_order=album_generated_order
    )

    new_album_generated.save()

    serializer = AlbumSerializer(album)
    return JsonResponse(serializer.data, safe=False)


@ api_view(['GET'])
@ authentication_classes([authentication.TokenAuthentication])
@ permission_classes([permissions.IsAuthenticated])
def get_rankings(request):

    generated_albums = AlbumUserHistory.objects.filter(
        user_generated=request.user.id).order_by("user_ranked_order")

    serializer = AlbumUserHistorySerializer(generated_albums, many=True)

    return JsonResponse(serializer.data, safe=False)


@ api_view(['POST'])
@ authentication_classes([authentication.TokenAuthentication])
@ permission_classes([permissions.IsAuthenticated])
def update_rankings(request):

    unsaved_rankings = json.loads(request.data["newListOrder"])

    generated_albums = AlbumUserHistory.objects.filter(
        user_generated=request.user.id).order_by("user_ranked_order")

    for album in generated_albums:

        if album.id in unsaved_rankings:

            index_pos = unsaved_rankings.index(album.id)
            album.user_ranked_order = index_pos + 1

    AlbumUserHistory.objects.bulk_update(
        generated_albums, ['user_ranked_order'])

    return JsonResponse({"message": "Thanks"})
