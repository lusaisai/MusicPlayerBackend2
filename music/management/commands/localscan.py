# coding=utf-8
from django.core.management.base import BaseCommand
from music.models import *
from os import listdir, chdir
from os.path import isfile, isdir
from MusicPlayerBackend2 import settings
import re


def is_song(name):
    return name.lower().endswith(".mp3") or name.lower().endswith(".m4a")


def music_filename_clean(name):
    name = re.sub(r'\.[^.]*$', '', name).strip()
    name = re.sub(r'^.*-', '', name).strip()
    name = re.sub(r'[0-9]+[. ]', '', name).strip()
    name = re.sub(ur'\[.*\]', '', name).strip()
    name = re.sub(ur'【.*】', '', name).strip()
    name = re.sub(ur'\(.*\)', '', name).strip()
    name = re.sub(ur'（.*）', '', name).strip()
    name = re.sub(r'\.[^.]*$', '', name).strip()
    return name


def clean_db():
    Song.objects.all().delete()
    Album.objects.all().delete()
    Artist.objects.all().delete()


def disk_scan():
    artists = []  # a list of Artists to be bulk inserted in db later
    albums = []  # a list of albums to be bulk inserted in db later
    songs = []  # a list of songs to be bulk inserted in db later

    chdir(settings.MUSIC_DIR)
    artist_names = [d.decode('GBK') for d in listdir(".") if isdir(d)]

    for artist_id, artist_name in enumerate(artist_names):
        artist = Artist(id=artist_id, name=artist_name)
        artists.append(artist)

        chdir(artist_name)
        album_names = [d.decode('GBK') for d in listdir(".") if isdir(d)]
        for album_id, album_name in enumerate(album_names):
            album_id += artist_id*100  # no one has more than 100 albums
            album = Album(id=album_id, name=album_name, artist=artist)
            albums.append(album)

            chdir(album_name)
            song_names = [s.decode('GBK') for s in listdir(".") if isfile(s) and is_song(s)]
            for song_id, song_name in enumerate(song_names):
                song_id += album_id * 200
                song = Song(id=song_id, name=music_filename_clean(song_name), file_name=song_name, album=album)
                songs.append(song)
            chdir("..")
        chdir("..")
    chdir("..")

    Artist.objects.bulk_create(artists)
    Album.objects.bulk_create(albums)
    Song.objects.bulk_create(songs)


class Command(BaseCommand):
    help = "populate the music database"

    def handle(self, *args, **options):
        clean_db()
        disk_scan()
