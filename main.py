import requests, sys
import time
import subprocess
base_url = "http://0.0.0.0:5000"
def menu():
    actions = {
        "1": extract_audio,
        "2": transcribe_audio,
        "3": list_audio_files,
        "0": exit
    }

    print("1. Extract audio from video")
    print("2. Transcribe audio")
    print("3. List available audio files")
    print("0. Exit")

    choice = input("Enter your choice: ")
    action = actions.get(choice)

    if action:
        action()
    else:
        print("Invalid choice. Try again.")

def extract_audio():
    videos_list = requests.get(f"{base_url}/v1/list/videos")
    message = videos_list.json()["message"]
    print(message)
    files = videos_list.json()["files"]

    for index, file in enumerate(files):
        print(f"{index+1}. {file}")
    try:
        choice = int(input("Enter the index of the audio file you want to transcribe:" ))
    except ValueError as e:
        print(e)
        return

    if choice == 0 or choice is None or choice == "":
        return
    if choice < 1 or choice > len(files):
        print("Invalid choice. Try again.")
        return
    video_path = files[choice-1]
    if check_audio_already_exists(video_path):
        print("Audio already extracted from this video.")
        choice = input("Do you want to extract audio again? (y/N): ")
        if choice.lower() != "y":
            return
    # video_path = input("Enter video path: ")
    output = requests.get(f"{base_url}/v1/extract/audio/", params={"filename": video_path})
    message = output.json()["message"]
    print(message)

def transcribe_audio():
    audio_files_list = requests.get(f"{base_url}/v1/list/audio")
    message = audio_files_list.json()["message"]
    print(message)
    files = audio_files_list.json()["files"]

    for index, file in enumerate(files):
        print(f"{index+1}. {file}")
    try:
        choice = int(input("Enter the index of the audio file you want to transcribe: "))
    except ValueError as e:
        print(e)
        return
    if choice == 0 or choice is None or choice == "":
        return
    if choice < 1 or choice > len(files):
        print("Invalid choice. Try again.")
        return
    audio_filename = files[choice-1]
    if check_srt_already_exists(audio_filename):
        print("SRT file already exists for this audio.")
        choice = input("Do you want to transcribe again? (y/N): ")
        if choice.lower() != "y":
            return
    # audio_filename = input("Enter audio file name: ")
    print("Transcribing audio...")
    output = requests.get(f"{base_url}/v1/transcribe/audio/", params={"filename": audio_filename})
    message = output.json()["message"]
    print(message)

def list_audio_files():
    output = requests.get(f"{base_url}/v1/list/audio")
    message = output.json()["message"]
    files = output.json()["files"]
    print(message)
    for index, file in enumerate(files):
        print(f"{index+1}. {file}")

def exit():
    print("Exiting the program.")
    choice = input("Do you wish to stop the server? (y/N): ")
    if choice.lower() == "y":
        output = subprocess.Popen(["docker", "compose", "down"])
        print("Server stopped.")
    else:
        print("Server is still running.")
    sys.exit()

def check_audio_already_exists(filename):
    output = requests.get(f"{base_url}/v1/list/audio")
    files = output.json()["files"]
    filename = filename.split(".")[-2] + ".wav"
    if filename in files:
        return True
    return False

def check_srt_already_exists(filename):
    output = requests.get(f"{base_url}/v1/list/srt")
    files = output.json()["files"]
    filename = filename.split(".")[-2] + ".srt"
    if filename in files:
        return True
    return False

if __name__ == "__main__":
    for _ in range(3):
        try:
            output = requests.get(f"{base_url}/")
            message = output.json()["message"]
            print(message)
            break
        except requests.exceptions.ConnectionError:
            print("Server is not running.")
            print("Please start the server before running this script.")
            print("Attempting to wait for the server...")
            time.sleep(1)
    else:
        print("Failed to connect to the server after 3 attempts.")
        choice = input("Do you wish to force start the server? (y/N): ")
        if choice.lower() == "y":  
            subprocess.Popen(["docker", "compose", "up", "-d"])
        else:
            sys.exit()
    while True:
        menu()
        print()
