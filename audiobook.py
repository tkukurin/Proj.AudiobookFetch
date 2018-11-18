#!/usr/bin/python

import youtube_dl
import sys


ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'download-archive': 'stats',
    'yes-playlist': True,
}


if len(sys.argv) == 1:
  print('Usage: audiobook.py [vid_ids]')
  sys.exit(1)

import requests
import re
def find_vids(playlist_url):
  url = 'https://youtube.com/playlist?list={}'.format(playlist_url)
  str_ = requests.get(url).text
  return [x[1] for x in re.findall(r'(watch.v=)([^&]*)', str_)]
  
vids = find_vids(sys.argv[1]) if sys.argv[1].startswith('PL') else sys.argv[1:]
vids = set(vids)

from multiprocessing import Pool
def download(v):
  with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    ydl.download([v])
  
with Pool(1) as p:
  vids = ['http://www.youtube.com/watch?v={}'.format(vid) for vid in vids]
  p.map(download, vids)


