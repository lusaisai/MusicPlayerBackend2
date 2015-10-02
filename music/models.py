from django.db import models
from MusicPlayerBackend2.settings import MUSIC_RESOURCE_HTTP_PREFIX
from pypinyin import lazy_pinyin


# Create your models here.
class ArtistManager(models.Manager):
    def pack_into_list(self, ids):
        data = []
        artists = self.model.objects.prefetch_related("album_set").in_bulk(ids)
        for artist in artists.values():
            data.append({
                "name": artist.name,
                "albums": [album.pack_data_into_dict() for album in artist.album_set.all()]
            })

        return data


class Artist(models.Model):
    name = models.CharField(max_length=100)
    objects = ArtistManager()

    def _get_pinyin_name(self):
        return "".join(lazy_pinyin(self.name))
    pinyin_name = property(_get_pinyin_name)

    def pack_data_into_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "pinyinName": self.pinyin_name
        }

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name


class AlbumManager(models.Manager):
    def pack_into_list(self, ids):
        data = []
        albums = self.model.objects.select_related('artist').prefetch_related("song_set").in_bulk(ids)
        for album in albums.values():
            data.append({
                "name": album.name,
                "songs": [song.pack_data_into_dict() for song in album.song_set.all()]
            })

        return data


class Album(models.Model):
    name = models.CharField(max_length=100)
    artist = models.ForeignKey(Artist)
    objects = AlbumManager()

    def _get_pinyin_name(self):
        return "".join(lazy_pinyin(self.name))
    pinyin_name = property(_get_pinyin_name)

    def pack_data_into_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "pinyinName": self.pinyin_name
        }

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name


class SongManager(models.Manager):
    def pack_into_list(self, ids):
        data = []
        songs = self.model.objects.select_related("album__artist").in_bulk(ids)
        for song in songs.values():
            data.append(song.pack_data_into_dict())

        return data


class Song(models.Model):
    name = models.CharField(max_length=100)
    file_name = models.CharField(max_length=100)
    album = models.ForeignKey(Album)
    objects = SongManager()

    def _get_pinyin_name(self):
        return "".join(lazy_pinyin(self.name))
    pinyin_name = property(_get_pinyin_name)

    def _get_url(self):
        album = self.album
        artist = album.artist
        return MUSIC_RESOURCE_HTTP_PREFIX + "/".join([artist.name, album.name, self.file_name])
    url = property(_get_url)

    def pack_data_into_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "artistName": self.album.artist.name,
            "albumName": self.album.name,
            "pinyinName": self.pinyin_name,
            "url": self.url
        }

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name


class Lyrics(models.Model):
    artist_name = models.CharField(max_length=100, db_index=True)
    album_name = models.CharField(max_length=100, db_index=True)
    song_name = models.CharField(max_length=100, db_index=True)
    content = models.TextField()

    def __str__(self):
        return self.content

    def __unicode__(self):
        return self.content


class Poem(models.Model):
    content = models.TextField()
    poet = models.CharField(max_length=100)

    def pack_data_into_dict(self):
        return {
            "content": self.content,
            "poet": self.poet
        }

    def __str__(self):
        return self.content

    def __unicode__(self):
        return self.content
