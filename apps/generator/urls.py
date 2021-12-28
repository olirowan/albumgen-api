from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import AlbumViewSet, generate_album, get_album, get_rankings, update_rankings

router = DefaultRouter()
router.register("albums", AlbumViewSet, basename="albums")

urlpatterns = [
    path('', include(router.urls)),
    path('album/generate', generate_album, name='generate_album'),
    path('album/get', get_album, name='get_album'),
    path('album/rankings', get_rankings, name='get_rankings'),
    path('album/update_rankings', update_rankings, name='update_rankings')
]
