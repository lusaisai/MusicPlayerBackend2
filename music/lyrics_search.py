# coding=utf-8
import urllib2
import json
import random
import zlib
import gzip
from StringIO import StringIO
import math
import re


# Kugou
def get_lrc_from_kugou(song_name, artist_name):
    lrc = ''
    try:
        data = search_from_kugou(song_name, artist_name)
        if data["total"] > 0:
            song = random.choice(data["songs"])
            lrc = download_lrc_from_kugou(song)
        else:
            data = search_from_kugou(song_name)
            if data["total"] > 0:
                song = random.choice(data["songs"])
                lrc = download_lrc_from_kugou(song)
    except IOError:
        pass

    return lrc


def search_from_kugou(song_name, artist_name=None):
    prefix = "http://lib9.service.kugou.com/websearch/index.php?page=1&pagesize=9&cmd=100&keyword="
    if artist_name:
        url_suffix = '%s-%s' % (artist_name, song_name)
    else:
        url_suffix = '%s' % song_name
    url = prefix + urllib2.quote(url_suffix.encode('utf-8'))
    request = urllib2.Request(url, headers={"Accept": "application/json"})
    response = urllib2.urlopen(request, timeout=2)
    data = json.load(response)
    return data["data"]


def download_lrc_from_kugou(song):
    prefix = "http://mobilecdn.kugou.com/new/app/i/krc.php?timelength=322000&type=1&cmd=200&open2close=-1&"
    url_suffix = 'keyword=%s-%s&hash=%s' % (
        urllib2.quote(song["singername"].encode('utf-8')),
        urllib2.quote(song["songname"].encode('utf-8')),
        song["hash"])
    url = prefix + url_suffix
    request = urllib2.Request(url, headers={"Accept": "text/html"})
    response = urllib2.urlopen(request, timeout=2)
    gzf = gzip.GzipFile(fileobj=StringIO(response.read()))
    data = gzf.read()
    return parse_binary_data_from_kugou(data)


def parse_binary_data_from_kugou(data):
    krc = ""
    zip_data = krc_hex_xor(data)
    if not zip_data:
        return krc
    else:
        krc = zlib.decompress(zip_data)
        return krc2lrc(krc)


def krc_hex_xor(data):
    enc_key = [0x40, 0x47, 0x61, 0x77, 0x5e, 0x32, 0x74, 0x47, 0x51, 0x36, 0x31, 0x2d, 0xce, 0xd2, 0x6e, 0x69]
    krc_data = []

    if not data[:4] == 'krc1':
        return ''
    else:
        for index, char in enumerate(data[4:]):
            krc_data.append(chr(ord(char) ^ enc_key[index % 16]))
        return ''.join(krc_data)


def krc2lrc(krc):
    lrc = re.sub(r'<[\d,\s]*>', '', krc)
    lrc = re.sub(r'\[(\d+),\s?(\d+)\]', time_replace, lrc)
    return lrc


def time_replace(match_obj):
    return "[%s]" % time_format(match_obj.group(1))


def time_format(time):
    time = math.fabs(float(time)/1000)
    hours = int(math.floor(time/3600))
    time -= hours * 3600
    minutes = int(math.floor(time/60))
    time -= minutes * 60
    seconds = int(math.floor(time))
    milliseconds = int((time - seconds) * 100)
    formatted = ''
    if hours:
        formatted += str(hours).zfill(2) + ":"
    formatted += str(minutes).zfill(2) + ":"
    formatted += str(seconds).zfill(2) + "."
    formatted += str(milliseconds).zfill(2)
    return formatted


if __name__ == '__main__':
    test_txt = get_lrc_from_kugou(u'品冠', u'越爱越配')
    print(test_txt)
