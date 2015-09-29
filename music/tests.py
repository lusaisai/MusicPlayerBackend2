# coding=utf-8
from django.test import TestCase
from music.models import *
from MusicPlayerBackend2.settings import MUSIC_RESOURCE_HTTP_PREFIX
import json


# Create your tests here.
class APITest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Artist.objects.bulk_create([
            Artist(id=1, name=u"品冠"),
            Artist(id=2, name=u"梁静茹")
        ])
        Album.objects.bulk_create([
            Album(id=1, name=u"爱到无可救药", artist_id=1),
            Album(id=2, name=u"未拆的礼物", artist_id=1),
            Album(id=3, name=u"勇气", artist_id=2)
        ])
        Song.objects.bulk_create([
            Song(id=1, name=u"Darling", file_name=u"Darling.mp3", album_id=1),
            Song(id=2, name=u"无可救药", file_name=u"无可救药.mp3", album_id=1),
            Song(id=3, name=u"执子之手", file_name=u"黄品冠 - 10.执子之手.m4a", album_id=2),
            Song(id=4, name=u"勇气", file_name=u"勇气.m4a", album_id=3)
        ])
        Poem.objects.bulk_create([
            Poem(content=u"多情自古伤离别 更那堪 冷落清秋节", poet=u"柳永"),
            Poem(content=u"今宵酒醒何处 杨柳岸 晚风 残月", poet=u"柳永")
        ])

    def setUp(self):
        self.maxDiff = None

    def tearDown(self):
        pass

    def test_home_page(self):
        response = self.client.get('/')
        self.assertEqual(302, response.status_code)
        self.assertEqual('http://testserver/static/index.html', response.url)

    def test_random_poem(self):
        response = self.client.get('/randompoem/')
        data = json.loads(response.content)
        self.assertGreater(len(data["content"]), 0)
        self.assertGreater(len(data["poet"]), 0)

    def test_all_artists(self):
        response = self.client.get('/artist/')
        expected = {
            "artists": [
                {
                    "id": 1,
                    "name": u'品冠',
                    "pinyinName": 'pinguan'
                },
                {
                    "id": 2,
                    "name": u'梁静茹',
                    "pinyinName": 'liangjingru'
                }
            ]
        }
        self.assertJSONEqual(response.content, expected)

    def test_some_artists(self):
        response = self.client.get('/artist/1,2/')
        data = json.loads(response.content)
        expected = {
            "artists": [
                {
                    "name": u"品冠",
                    "albums": [
                        {
                            "id": 1,
                            "name": u"爱到无可救药",
                            "pinyinName": "aidaowukejiuyao"
                        },
                        {
                            "id": 2,
                            "name": u"未拆的礼物",
                            "pinyinName": "weichaidiliwu"
                        }
                    ]
                },
                {
                    "name": u"梁静茹",
                    "albums": [
                        {
                            "id": 3,
                            "name": u"勇气",
                            "pinyinName": "yongqi"
                        }
                    ]
                }
            ]
        }
        self.assertDictEqual(expected, data)

    def test_an_artist(self):
        response = self.client.get('/artist/1/')
        data = json.loads(response.content)
        expected = {
            "artists": [
                {
                    "name": u"品冠",
                    "albums": [
                        {
                            "id": 1,
                            "name": u"爱到无可救药",
                            "pinyinName": "aidaowukejiuyao"
                        },
                        {
                            "id": 2,
                            "name": u"未拆的礼物",
                            "pinyinName": "weichaidiliwu"
                        }
                    ]
                }
            ]
        }
        self.assertDictEqual(expected, data)

    def test_no_artist(self):
        response = self.client.get('/artist/10/')
        data = json.loads(response.content)
        expected = {
            "artists": []
        }
        self.assertDictEqual(expected, data)

    def test_an_album(self):
        response = self.client.get('/album/3/')
        data = json.loads(response.content)
        expected = {
            "albums": [
                {
                    "name": u"勇气",
                    "songs": [
                        {
                            "id": 4,
                            "name": u"勇气",
                            "artistName": u"梁静茹",
                            "albumName": u"勇气",
                            "pinyinName": "yongqi",
                            "url": MUSIC_RESOURCE_HTTP_PREFIX + u"梁静茹/勇气/勇气.m4a"
                        }
                    ]
                }
            ]
        }
        self.assertDictEqual(expected, data)

    def test_some_albums(self):
        response = self.client.get('/album/2,3/')
        data = json.loads(response.content)
        expected = {
            "albums": [
                {
                    "name": u"未拆的礼物",
                    "songs": [
                        {
                            "id": 3,
                            "name": u"执子之手",
                            "pinyinName": "zhizizhishou",
                            "albumName": u"未拆的礼物",
                            "artistName": u"品冠",
                            "url": MUSIC_RESOURCE_HTTP_PREFIX + u"品冠/未拆的礼物/黄品冠 - 10.执子之手.m4a"
                        }
                    ]
                },
                {
                    "name": u"勇气",
                    "songs": [
                        {
                            "id": 4,
                            "name": u"勇气",
                            "pinyinName": "yongqi",
                            "albumName": u"勇气",
                            "artistName": u"梁静茹",
                            "url": MUSIC_RESOURCE_HTTP_PREFIX + u"梁静茹/勇气/勇气.m4a"
                        }
                    ]
                }
            ]
        }
        self.assertDictEqual(expected, data)

    def test_no_album(self):
        response = self.client.get('/album/30/')
        data = json.loads(response.content)
        expected = {
            "albums": []
        }
        self.assertDictEqual(expected, data)

    def test_lyrics(self):
        response = self.client.get('/lyrics/4/')
        data1 = json.loads(response.content)
        response = self.client.get('/reloadlyrics/4/')
        data2 = json.loads(response.content)

        self.assertIn("content", data1)
        self.assertIn("content", data2)

    def test_random_songs(self):
        response = self.client.get('/randomsongs/2/')
        data = json.loads(response.content)

        self.assertEqual(2, len(data["songs"]))
        one_song = data["songs"][0]
        self.assertIn("id", one_song)
        self.assertIn("name", one_song)
        self.assertIn("pinyinName", one_song)
        self.assertIn("albumName", one_song)
        self.assertIn("artistName", one_song)
        self.assertIn("url", one_song)
