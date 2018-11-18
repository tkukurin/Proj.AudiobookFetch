import os
import re
import shutil
from collections import defaultdict

def folder_name(f):
  matches = [
    r'(.*) part ',
    r'(.*) audiobook \d+',
    r'(.*) \d+/\d+',
    r'(.*).mp3',]

  def group_extract(m): 
    matched = re.match(m, f.lower())
    return matched.group(1) if matched else None

  return next(filter(lambda x: x, map(group_extract, matches)), None)


partified_files = defaultdict(list)
for f in filter(lambda x: x.endswith('.mp3'), os.listdir('.')):
  partified_files[folder_name(f)].append(f)

for folder, files in partified_files.items():
  os.mkdir(folder)
  for f in files:
    shutil.move(f, folder)

