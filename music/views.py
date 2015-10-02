from django.http import JsonResponse
from music.models import *
from MusicPlayerBackend2 import settings
from django.shortcuts import redirect, get_object_or_404
from lyrics_search import *


# Create your views here.
def home(request):
    return redirect(settings.STATIC_URL + "index.html")


def artists(request):
    data = {"artists": []}

    for obj in Artist.objects.all():
        data["artists"].append(obj.pack_data_into_dict())

    return JsonResponse(data)


def artist(request, artist_ids):
    objs = Artist.objects.pack_into_list(artist_ids.split(','))
    data = {"artists": objs}

    return JsonResponse(data)


def album(request, album_ids):
    albums = Album.objects.pack_into_list(album_ids.split(','))
    data = {"albums": albums}

    return JsonResponse(data)


def random_songs(request, number):
    number = int(number)
    data = {"songs": []}
    ids = [song.id for song in Song.objects.only("id").order_by('?')[:number]]
    data["songs"] = Song.objects.pack_into_list(ids)

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


def random_poem(request):
    poem = Poem.objects.order_by('?').first()
    return JsonResponse(poem.pack_data_into_dict())
