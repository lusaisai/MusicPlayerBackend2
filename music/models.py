from django.db import models


# Create your models here.
class Artist(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Album(models.Model):
    name = models.CharField(max_length=100)
    artist = models.ForeignKey(Artist)

    def __str__(self):
        return self.name


class Song(models.Model):
    name = models.CharField(max_length=100)
    file_name = models.CharField(max_length=100)
    album = models.ForeignKey(Album)

    def __str__(self):
        return self.name


class Lyric(models.Model):
    artist = models.CharField(max_length=100)
    album = models.CharField(max_length=100)
    song = models.CharField(max_length=100)
    content = models.TextField()

    def __str__(self):
        return self.content


class Poem(models.Model):
    content = models.TextField()
    poet = models.CharField(max_length=100)

    def __str__(self):
        return self.content
