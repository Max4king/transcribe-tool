import moviepy.editor as mp

default_directory = "output/audio/"


def extract_audio(video_path, file_name='output.wav'):
    video = mp.VideoFileClip(video_path)
    audio = video.audio
    if file_name == 'output.wav':
        audio.write_audiofile(default_directory + file_name)
    else:
        audio.write_audiofile(file_name)