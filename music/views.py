from django.http import JsonResponse, Http404
from django.core.exceptions import ObjectDoesNotExist
from music.models import *
from MusicPlayerBackend2 import settings
from pypinyin import lazy_pinyin
from django.shortcuts import redirect


# Create your views here.
def home(request):
    return redirect(settings.STATIC_URL + "index.html")


def artists(request):
    data = {"artists": []}
    for obj in Artist.objects.all():
        data["artists"].append({
            "id": obj.id,
            "name": obj.name,
            "pinyinName": "".join(lazy_pinyin(obj.name))
        })
    return JsonResponse(data)


def artist(request, artist_id):
    try:
        a = Artist.objects.get(id=artist_id)
    except ObjectDoesNotExist:
        raise Http404("Artist does not exist.")

    data = {
        "artist": a.name,
        "albums": []
    }

    for obj in a.album_set.all():
        data["albums"].append({
            "id": obj.id,
            "name": obj.name,
            "pinyinName": "".join(lazy_pinyin(obj.name))
        })

    return JsonResponse(data)


def album(request, album_id):
    try:
        a = Album.objects.get(id=album_id)
    except ObjectDoesNotExist:
        raise Http404("Album does not exist.")

    data = {
        "album": a.name,
        "songs": []
    }

    for obj in a.song_set.all():
        data["songs"].append({
            "id": obj.id,
            "name": obj.name,
            "artistName": a.artist.name,
            "albumName": a.name,
            "pinyinName": "".join(lazy_pinyin(obj.name)),
            "url": settings.MUSIC_RESOURCE_HTTP_PREFIX + "/".join([a.artist.name, a.name, obj.file_name])
        })

    return JsonResponse(data)
