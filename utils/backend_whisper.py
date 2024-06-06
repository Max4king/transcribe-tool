from faster_whisper import WhisperModel
import os

model_size = "large-v2"


def transcribe_audio(audio_path):
    # Run on GPU with FP16
    model = WhisperModel(model_size, device="cuda", compute_type="float16")


    if not os.path.exists(f"output/audio/{audio_path}"):
        raise FileNotFoundError("Audio file not found")

    segments, info = model.transcribe(f"output/audio/{audio_path}", beam_size=5)
    filename, ext = os.path.splitext(audio_path)

    
    print("Detected language '%s' with probability %f" % (info.language, info.language_probability))
    with open(f"output/srt/{filename}.srt", "w") as srt_file:
        i = 1
        for segment in segments:
            print("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))
            srt_file.write(f"{i}\n")
            srt_file.write(f"{format_srt_time(segment.start)} --> {format_srt_time(segment.end)}\n")
            srt_file.write(f"{segment.text}\n\n")
            i += 1
    
    print(f"Transcription {filename}.srt has been saved")

def format_srt_time(sec):
    # Convert seconds to hours, minutes, seconds, milliseconds
    hours, remainder = divmod(sec, 3600)
    minutes, remainder = divmod(remainder, 60)
    seconds, milliseconds = divmod(remainder, 1)
    milliseconds *= 1000

    # Return formatted string
    return "{:02}:{:02}:{:02},{:03}".format(int(hours), int(minutes), int(seconds), int(milliseconds))