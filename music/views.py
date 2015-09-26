from django.http import JsonResponse
from music.models import *
from MusicPlayerBackend2 import settings
from pypinyin import lazy_pinyin
from django.shortcuts import redirect, get_object_or_404
from lyrics_search import *


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
    a = get_object_or_404(Artist, id=artist_id)

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
    a = get_object_or_404(Album, id=album_id)

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


def random_songs(request, number):
    number = int(number)
    data = {"songs": []}
    songs = Song.objects.order_by('?')[:number]
    for song in songs:
        artist_name = song.album.artist.name
        album_name = song.album.name
        data["songs"].append({
            "id": song.id,
            "name": song.name,
            "artistName": artist_name,
            "albumName": album_name,
            "pinyinName": "".join(lazy_pinyin(song.name)),
            "url": settings.MUSIC_RESOURCE_HTTP_PREFIX + "/".join([artist_name, album_name, song.file_name])
        })
    return JsonResponse(data)


def lyrics(request, song_id, need_reloaded=False):
    song = get_object_or_404(Song, id=song_id)
    song_name = song.name
    artist_name = song.album.artist.name

    lrc, created = Lyrics.objects.get_or_create(artist_name__iexact=artist_name, song_name__iexact=song_name)
    if created or lrc.content == "" or need_reloaded:
        lrc.content = get_lrc_from_kugou(song_name, artist_name)
        lrc.artist_name = artist_name
        lrc.song_name = song_name
        lrc.save()
    else:
        pass
    return JsonResponse({"content": lrc.content})


def reload_lyrics(request, song_id):
    return lyrics(request, song_id, True)
