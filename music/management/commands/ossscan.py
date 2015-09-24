from django.core.management import BaseCommand
from oss import oss_xml_handler
from MusicPlayerBackend2.oss_settings import *
from oss.oss_api import *
from localscan import is_song, music_filename_clean, clean_db
from music.models import *


class Command(BaseCommand):
    help = "populate the music database"

    def handle(self, *args, **options):
        clean_db()

        oss = OssAPI(ENDPOINT, ID, KEY)

        prefix = 'music/'
        artists_xml = oss_xml_handler.GetBucketXml(
            oss.list_bucket(BUCKET, prefix=prefix, maxkeys=1000).read())
        for raw_path in artists_xml.content_list:
            path = raw_path.key.replace(prefix, '')
            if path.endswith('.jpg'):
                continue
            path_info = [li for li in path.split('/') if len(li) > 0]

            # artist
            if len(path_info) == 1:
                Artist.objects.get_or_create(name=path_info[0])
            elif len(path_info) == 2:
                artist, created = Artist.objects.get_or_create(name=path_info[0])
                Album.objects.get_or_create(name=path_info[1], artist=artist)
            elif len(path_info) == 3:
                artist, created = Artist.objects.get_or_create(name=path_info[0])
                album, created = Album.objects.get_or_create(name=path_info[1], artist=artist)
                if is_song(path_info[2]):
                    Song.objects.get_or_create(name=music_filename_clean(path_info[2]),
                                               file_name=path_info[2], album=album)
