from fastapi import FastAPI
from utils.backend_whisper import transcribe_audio
from utils.extract_audio import extract_audio
import os
import uvicorn
app = FastAPI()


@app.get("/")
def connection():
    return {"message": "Connection successful"}

@app.get("/v1/extract/audio/video_path={video_path}")
def extract_audio_from_video(video_path: str):
    extract_audio(video_path)
    return {"message": "Audio extracted successfully"}

@app.get("/v1/transcribe/audio/audio_filename={audio_filename}")
def transcribe_audio_file(audio_filename: str):
    try:
        transcribe_audio(audio_filename)
    except FileNotFoundError:
        return {"message": "Audio file not found"}
    return {"message": "Transcription completed successfully"}

@app.get("/v1/list/audio_files")
def list_audio_files():
    return {"message": "Available audio files:", "files": os.listdir("output/audio")}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)