import moviepy.editor as mp
import os
default_directory = "output/audio/"


def extract_audio(video_path, file_name=None):
    if os.path.exists(video_path) is False:
        raise FileNotFoundError("Video file not found")
    video = mp.VideoFileClip(video_path)
    audio = video.audio
    if file_name is None:
        audio.write_audiofile(default_directory + video_path.split("/")[-1].split(".")[0] + ".wav")
    else:
        audio.write_audiofile(file_name)