import requests, sys

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
    sys.exit()

if __name__ == "__main__":
    try:
        output = requests.get(f"{base_url}/")
        message = output.json()["message"]
        print(message)
    except requests.exceptions.ConnectionError:
        print("Server is not running. Please start the server before running this script.")
        sys.exit()
    while True:
        menu()
        print()