import random
import numpy as np
import time
import os
import datetime

from uploader import upload

from moviepy.editor import * # type: ignore
from moviepy.video.fx.all import crop # type: ignore
from moviepy.audio.fx.volumex import volumex

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

posting_times = {
    0:[ # Monday
        [3,30],
        [6,30],
        [9,0],
        [11,45],
        [17,15]
    ],
    1:[ # Tuesday
        [5,0],
        [6,30],
        [7,30],
        [8,30],
        [13,0]

    ],
    2:[ # Wednesday
        [5,0],
        [6,30],
        [8,0],
        [16,0],
        [20,45]
    ],
    3:[ # Thursday
        [6,0],
        [8,0],
        [9,0],
        [13,0],
        [21,0]
    ],
    4:[ # Friday
        [6,15],
        [7,30],
        [9,30],
        [21,30],
        [13,0]
    ],
    5:[ # Saturday
        [12,30],
        [13,30],
        [14,30],
        [15,45],
        [19,15]
    ],
    6:[ #Sunday
        [3,30],
        [5,45],
        [7,45],
        [10,0],
        [14,0]
    ]
}
accounts = [4, 2, 3]

CLIP_LEN = 67
FUNNY_CLIP = "copy.mp4"
VIDEOS_DIRECTORY = f"/media/{os.getlogin()}/MOVIE/videos/"

def create_image(text, offset):

    font = ImageFont.truetype("font.ttf", size=60)
    w, h = font.getsize(text)

    img = Image.new('RGB', (720, 386), (0, 0, 0))
    d = ImageDraw.Draw(img)
    W, H = img.size
    d.text((W/2,H/2 + offset), text, fill=(200, 200, 200), font=font, anchor="mm")

    return np.asarray(img)

def create_clips(location, clip_length):
    video = VideoFileClip(location)
    cursor = 0
    part = 1

    while cursor < video.duration:
        random_addition = random.randint(0,40)
        if video.duration < (cursor + clip_length + 26 + random_addition):
            clip = VideoFileClip(location).subclip(cursor, video.duration)
        else:
            clip = VideoFileClip(location).subclip(cursor, cursor + random_addition + clip_length)

        clip = crop(clip, width=clip.w-260, x_center=clip.w/2)
        clip = clip.resize(width=720).margin(top=386, bottom=386)

        ''' # Temp Clip Code

        temp = VideoFileClip(FUNNY_CLIP).without_audio()
        random_cursor = random.randint(0, int(temp.duration) - int(clip.duration) - 10)
        temp = crop(temp, width=temp.w-584, x_center=temp.w/2)
        temp = temp.resize(width= 720).subclip(random_cursor, random_cursor + clip.duration)
        '''

        part_image = ImageClip(create_image(f"Part {part}", -100), duration=clip.duration)
        title_image = ImageClip(create_image(location.split(".")[0], 100), duration=clip.duration)

        v = CompositeVideoClip([clip.set_position(("center", "top")), part_image.set_position(("center", "bottom")), title_image.set_position(("center", "top"))])

        v.write_videofile(f"./clips/part {part} #foryou #movie.mp4", preset="ultrafast")

        cursor += clip.duration
        part += 1
        
        clip.close()
        part_image.close()
        title_image.close()
        v.close()

    video.close()
    

if __name__ == "__main__":
    if not os.path.isdir('clips'):
        os.makedirs('clips')
    while True:
        clips_directory = os.listdir("./clips")

        if len(clips_directory) == 0:
            videos_directory = os.listdir(VIDEOS_DIRECTORY)
            if len(videos_directory) > 0:
                cur_file = f"{VIDEOS_DIRECTORY}/{videos_directory[0]}"
                create_clips(cur_file, CLIP_LEN)
                os.remove(cur_file)
            else:
                break
        
        while len(clips_directory) > 0:
            time_now = datetime.datetime.now()
            print(time_now)

            if [time_now.hour, time_now.minute] in posting_times[time_now.weekday()]:
                cur_clip = clips_directory[0]

                for i in accounts:
                    upload(cur_clip, i)
                    time.sleep(120)

                os.remove(f"./clips/{cur_clip}")

            time.sleep(10)
        time.sleep(30)
