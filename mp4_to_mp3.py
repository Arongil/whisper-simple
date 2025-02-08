import os
import sys
from moviepy.editor import VideoFileClip

if __name__ == "__main__":
    print(sys.argv)
    if len(sys.argv) == 1:
        print("Please pass in a directory with mp4 files to convert.")
        exit()

    for dirname in sys.argv[1:]:
        filenames = os.listdir(dirname)
        for filename in filenames:
            root, ext = os.path.splitext(filename)
            if ext.lower() != ".mp4" or f"{root}.mp3" in filenames:
                continue  # either not an mp4 or file has already been converted

            video = VideoFileClip(f"{dirname}/{filename}")
            video.audio.write_audiofile(f"{dirname}/{root}.mp3", bitrate="64k")
