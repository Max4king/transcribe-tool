from fastapi import FastAPI
from utils.backend_whisper import transcribe_audio
from utils.extract_audio import extract_audio
import os
import uvicorn
app = FastAPI()


@app.get("/")
def connection():
    return {"message": "Connection successful"}

@app.get("/v1/list/videos")
def list_videos():
    return {"message": "Available videos:", "files": os.listdir("input")}

@app.get("/v1/extract/audio/")
def extract_audio_from_video(filename: str):
    full_path = "input/" + filename
    try:
        extract_audio(full_path)
    except FileNotFoundError:
        return {"message": "Video file not found"}
    return {"message": "Audio extracted successfully"}

@app.get("/v1/transcribe/audio/")
def transcribe_audio_file(filename: str):
    try:
        transcribe_audio(filename)
    except FileNotFoundError:
        return {"message": "Audio file not found"}
    return {"message": "Transcription completed successfully"}

@app.get("/v1/list/audio")
def list_audio_files():
    return {"message": "Available audio files:", "files": os.listdir("output/audio")}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)