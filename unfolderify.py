import os
import shutil

for folder in filter(os.path.isdir, os.listdir('.')):
  for file_ in os.listdir(folder):
    shutil.move(os.path.join(folder, file_), '.')
  if len(os.listdir(folder)) == 0:
    shutil.rmtree(folder)
