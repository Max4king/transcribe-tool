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
    choice = int(input("Enter the index of the video you want to extract audio from: "))
    if choice < 1 or choice > len(files):
        print("Invalid choice. Try again.")
        return
    video_path = files[choice-1]
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
    choice = int(input("Enter the index of the audio file you want to transcribe: "))
    if choice < 1 or choice > len(files):
        print("Invalid choice. Try again.")
        return
    audio_filename = files[choice-1]
    # audio_filename = input("Enter audio file name: ")
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
            time.sleep(0.5)
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