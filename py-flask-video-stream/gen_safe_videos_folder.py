"""
Generate a set of safe-for-viewing videos from the CORRECT-ly predected videos.
Input - folder with correctly predicted videos
Input - activities for safe viewing
Output - folder containing safe videos"""


import shutil
import subprocess
import os
from os import listdir
from os.path import isfile, join
from pudb import set_trace

set_trace()
dest_folder = 'videos_safe_viewing'
source_folder = 'videos_correct'

with open('safe_categories.txt') as f:
    categories = f.readlines()
    categories = [category.strip() for category in categories]
print(categories)

video_files = [f for f in listdir(source_folder) if isfile(join(source_folder, f))]

# recreate the dest folder
dir = dest_folder
if os.path.exists(dir):
    shutil.rmtree(dir)
os.makedirs(dir)

for video_file in video_files:
    category = video_file.split('_')[1]
    if category in categories:
        source_filepath = os.path.join(source_folder, video_file)
        dest_filepath = os.path.join(dest_folder, video_file)
        print('cp', source_filepath, dest_filepath)
        subprocess.call(['cp', source_filepath, dest_filepath])
