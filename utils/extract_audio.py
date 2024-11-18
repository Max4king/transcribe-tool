import moviepy.editor as mp
import os
import ffmpeg

input_directory = "input/"
default_audio = "output/audio/"
default_srt = "output/srt/"

def extract_audio(video_path, file_name=None):
    if os.path.exists(video_path) is False:
        raise FileNotFoundError("Video file not found")
    video = mp.VideoFileClip(video_path)
    audio = video.audio
    if file_name is None:
        audio.write_audiofile(
            default_audio + os.path.splitext(os.path.basename(video_path))[0] + ".wav"
        )
    else:
        audio.write_audiofile(file_name)


def convert_ass_to_srt(ass_filename):
    """
    Convert ASS subtitle file to SRT subtitle file using ffmpeg-python
    """
    ass_filename = input_directory + ass_filename
    if not os.path.exists(ass_filename):
        print(f"File {ass_filename} does not exist.")
        return

    srt_filename = os.path.join(default_srt, os.path.splitext(os.path.basename(ass_filename))[0] + '.srt')
    ffmpeg.input(ass_filename).output(srt_filename).run()


def time_str_to_seconds(time_str):
    h, m, s = map(float, time_str.replace(',', '.').split(':'))
    return h * 3600 + m * 60 + s


def condense_audio(audio_filename, srt_filename):
    """
    Condense the audio file based on the srt file by removing non-speaking parts.
    Returns the path to the condensed audio file.
    """
    audio_filename = default_audio + audio_filename
    srt_filename = default_srt + srt_filename

    if not os.path.exists(audio_filename):
        raise FileNotFoundError("Audio file not found")
    if not os.path.exists(srt_filename):
        raise FileNotFoundError("SRT file not found")

    # Generate condensed audio filename using proper path handling
    base_name, _ = os.path.splitext(audio_filename)
    condensed_audio_filename = f"{base_name}_condensed.wav"

    audio = mp.AudioFileClip(audio_filename)
    speech_times = []

    # Parse the SRT file to get speech segments
    with open(srt_filename, "r") as srt_file:
        lines = srt_file.readlines()
        index = 0
        while index < len(lines):
            line = lines[index].strip()
            if not line:
                index += 1
                continue
        
            index += 1  # Skip sequence number
            if index >= len(lines):
                break
        
            # Parse timestamp line
            time_line = lines[index].strip()
            if " --> " not in time_line:
                index += 1
                continue
        
            start_str, end_str = time_line.split(" --> ")
            start_sec = time_str_to_seconds(start_str)
            end_sec = time_str_to_seconds(end_str)
            speech_times.append((start_sec, end_sec))
            index += 1  # Move to the next entry
        
    # Concatenate speech segments
    condensed_audio = mp.concatenate_audioclips(
        [audio.subclip(start, end) for start, end in speech_times]
    )
    condensed_audio.write_audiofile(condensed_audio_filename)
    
    return condensed_audio_filename
