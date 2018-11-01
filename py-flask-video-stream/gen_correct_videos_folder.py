import shutil
import subprocess
import os

dest_folder = 'videos_correct'
source_folder = 'videos'

with open('results.txt') as f:
    files = f.readlines()
    files = [file.strip() for file in files]
print(files)

# recreate the dest folder
dir = dest_folder
if os.path.exists(dir):
    shutil.rmtree(dir)
os.makedirs(dir)

for file in files:
    pieces = file.split(' ')
    if pieces[1] == 'correct':
        source_filepath = os.path.join(source_folder, pieces[0]+'.webm')
        dest_filepath = os.path.join(dest_folder, pieces[0]+'.webm')
        print('cp', source_filepath, dest_filepath)
        subprocess.call(['cp', source_filepath, dest_filepath])
        
