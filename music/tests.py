# coding=utf-8
from django.test import TestCase
import requests
from MusicPlayerBackend2.settings import MUSIC_RESOURCE_HTTP_PREFIX


# Create your tests here.
class APITest(TestCase):
    def setUp(self):
        self.prefix = 'http://localhost:8000/'
        self.maxDiff = None

    def tearDown(self):
        pass

    def test_all_artists(self):
        data = requests.get(self.prefix + 'artist/').json()
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
        self.assertDictEqual(expected, data)

    def test_an_artist(self):
        data = requests.get(self.prefix + 'artist/1/').json()
        expected = {
            "artist": u"品冠",
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
        self.assertDictEqual(expected, data)

    def test_no_artist(self):
        r = requests.get(self.prefix + 'artist/10/')
        self.assertEqual(404, r.status_code)

    def test_an_album(self):
        data = requests.get(self.prefix + 'album/3/').json()
        expected = {
            "album": u"勇气",
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
        self.assertDictEqual(expected, data)

    def test_some_albums(self):
        data = requests.get(self.prefix + 'album/2,3/').json()
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
        r = requests.get(self.prefix + 'album/30/')
        self.assertEqual(404, r.status_code)

    def test_lyrics(self):
        data1 = requests.get(self.prefix + 'lyrics/4/').json()
        data2 = requests.get(self.prefix + 'reloadlyrics/4/').json()
        self.assertIn(u"我们都需要勇气", data1["content"])
        self.assertIn(u"我们都需要勇气", data2["content"])

    def test_random_songs(self):
        data = requests.get(self.prefix + 'randomsongs/2/').json()
        self.assertEqual(2, len(data["songs"]))
        one_song = data["songs"][0]
        self.assertIn("id", one_song)
        self.assertIn("name", one_song)
        self.assertIn("pinyinName", one_song)
        self.assertIn("albumName", one_song)
        self.assertIn("artistName", one_song)
        self.assertIn("url", one_song)
