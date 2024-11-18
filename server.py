from fastapi import FastAPI, HTTPException
from utils.backend_whisper import transcribe_audio
from utils.extract_audio import extract_audio, convert_ass_to_srt, condense_audio
import os
import uvicorn
from time import time
from pydantic import BaseModel

app = FastAPI()


class ASSFile(BaseModel):
    ass_filename: str


class CondenseRequest(BaseModel):
    audio_filename: str
    srt_filename: str


@app.get("/")
def connection():
    return {"message": "Connection successful"}


@app.get("/v1/videos")
def list_videos():
    return {"message": "Available videos:", "files": os.listdir("input")}


@app.get("/v1/audios/extract")
def extract_audio_from_video(filename: str):
    start_time = time()
    full_path = "input/" + filename
    try:
        extract_audio(full_path)
    except FileNotFoundError:
        return {"message": "Video file not found"}
    end_time = time()
    print(f"Time taken: {end_time-start_time}")
    return {"message": "Audio extracted successfully"}


@app.get("/v1/audios/transcribe")
def transcribe_audio_file(filename: str):
    start_time = time()
    try:
        transcribe_audio(filename)
    except FileNotFoundError:
        return {"message": "Audio file not found"}
    end_time = time()
    print(f"Time taken: {end_time-start_time}")
    return {"message": "Transcription completed successfully"}


@app.get("/v1/audios")
def list_audio_files():
    return {"message": "Available audio files:", "files": os.listdir("output/audio")}


@app.get("/v1/srt/list")
def list_srt_files():
    return {"message": "Available SRT files:", "files": os.listdir("output/srt")}


@app.post("/v1/ass/to/srt")
def convert_ass_to_srt_endpoint(ass_file: ASSFile):
    ass_filename = ass_file.ass_filename
    try:
        convert_ass_to_srt(ass_filename)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Ass file not found.")
    return {"message": "Ass file converted successfully"}


@app.post("/v1/audios/condense")
def condense_audio_files(request: CondenseRequest):
    audio_filename = request.audio_filename
    srt_filename = request.srt_filename
    try:
        result = condense_audio(audio_filename=audio_filename, srt_filename=srt_filename)
    except ZeroDivisionError as e:
        raise HTTPException(status_code=400,detail=str(e) )
    return {"message": f"Audio condensed successfully. File named {result}"}


@app.get("/v1/input")
def list_input_file():
    return {"message": "Available input files:", "files": os.listdir("input")}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)
