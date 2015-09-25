from django.http import JsonResponse, Http404
from django.core.exceptions import ObjectDoesNotExist
from music.models import *
from MusicPlayerBackend2 import settings
from pypinyin import lazy_pinyin
from django.shortcuts import redirect
import urllib2
import json
import random


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


# see http://gecimi.readthedocs.org/en/latest/ for source lrc data
def lyrics(request, song_id, need_reloaded=False):
    try:
        song = Song.objects.get(id=song_id)
        song_name = song.name
        artist_name = song.album.artist.name
    except ObjectDoesNotExist:
        raise Http404("Song does not exist.")

    lrc, created = Lyrics.objects.get_or_create(artist_name__iexact=artist_name, song_name__iexact=song_name)
    if created or lrc.content == "" or need_reloaded:
        lrc.content = get_lrc_from_gecimi(song_name, artist_name)
        lrc.artist_name = artist_name
        lrc.song_name = song_name
        lrc.save()
    else:
        pass
    return JsonResponse({"content": lrc.content})


def reload_lyrics(request, song_id):
    return lyrics(request, song_id, True)


def get_lrc_from_gecimi(song_name, artist_name):
    prefix = u'http://geci.me/api/lyric/'
    lrc = ''
    try:
        url = prefix + '%s/%s' % (song_name, artist_name)
        lrc = download_lrc(url)
        if lrc != "":
            return lrc
        else:
            url = prefix + '%s' % song_name
            lrc = download_lrc(url)
    except IOError:
        pass

    return lrc


def download_lrc(url):
    lrc = ''
    response = urllib2.urlopen(url.encode('utf-8'), timeout=2)
    data = json.load(response)
    if data["count"] > 0:
        url = random.choice(data["result"])["lrc"]
        lrc = urllib2.urlopen(url, timeout=2).read().decode('utf-8')
    return lrc
