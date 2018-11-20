#!/usr/bin/python

import youtube_dl
import sys
import requests
import re
import itertools as it
import multiprocessing as mp


ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'download-archive': 'stats',
}

def find_vids(playlist_id):
  url = 'https://youtube.com/playlist?list={}'.format(playlist_id)
  str_ = requests.get(url).text
  return [x[1] for x in re.findall(r'(watch.v=)([^&]*)', str_)]
  

def download(v):
  with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    ydl.download([v])


def urlfmt(url_or_vid):
  fmt = 'http://www.youtube.com/watch?v={}'
  return url_or_vid \
    if 'youtube.com' in url_or_vid \
    else fmt.format(url_or_vid)


def to_full_url(vid):
  return find_vids(vid) \
    if vid.startswith('PL') \
    else [urlfmt(vid)]


if __name__ == '__main__':
  if len(sys.argv) == 1:
    print('Usage: audiobook.py [vid_ids]')
    print('If name starts with PL, assumes playlist')
    sys.exit(1)

  vids = it.chain(*map(to_full_url, sys.argv[1:]))
  with mp.Pool(1) as p:
    p.map(download, set(vids))


