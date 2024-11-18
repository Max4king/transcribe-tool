import requests, sys
import time
import subprocess
import os

base_url = "http://0.0.0.0:5000"


def menu():
    actions = {
        "1": extract_audio,
        "2": transcribe_audio,
        "3": list_audio_files,
        "4": condense_audio,
        "5": list_input_files,
        "6": convert_ass_to_srt,
        "0": exit,
    }

    print("1. Extract audio from video")
    print("2. Transcribe audio")
    print("3. List available audio files")
    print("4. Condense audio")
    print("5. List input files")
    print("6. Convert ass file to srt file")
    print("0. Exit")

    choice = input("Enter your choice: ")
    action = actions.get(choice)

    if action:
        action()
    else:
        print("Invalid choice. Try again.")


def extract_audio():
    videos_list = requests.get(f"{base_url}/v1/videos")
    message = videos_list.json()["message"]
    print(message)
    files = videos_list.json()["files"]

    for index, file in enumerate(files):
        print(f"{index+1}. {file}")
    try:
        choice = int(input("Enter the index of the audio file you want to transcribe:"))
    except ValueError as e:
        print(e)
        return

    if choice == 0 or choice is None or choice == "":
        return
    if choice < 1 or choice > len(files):
        print("Invalid choice. Try again.")
        return
    video_path = files[choice - 1]
    if check_audio_already_exists(video_path):
        print("Audio already extracted from this video.")
        choice = input("Do you want to extract audio again? (y/N): ")
        if choice.lower() != "y":
            return
    # video_path = input("Enter video path: ")
    output = requests.get(
        f"{base_url}/v1/audios/extract/", params={"filename": video_path}
    )
    message = output.json()["message"]
    print(message)


def transcribe_audio():
    audio_files_list = requests.get(f"{base_url}/v1/audios")
    message = audio_files_list.json()["message"]
    print(message)
    files = audio_files_list.json()["files"]

    for index, file in enumerate(files):
        print(f"{index+1}. {file}")
    try:
        choice = int(
            input("Enter the index of the audio file you want to transcribe: ")
        )
    except ValueError as e:
        print(e)
        return
    if choice == 0 or choice is None or choice == "":
        return
    if choice < 1 or choice > len(files):
        print("Invalid choice. Try again.")
        return
    audio_filename = files[choice - 1]
    if check_srt_already_exists(audio_filename):
        print("SRT file already exists for this audio.")
        choice = input("Do you want to transcribe again? (y/N): ")
        if choice.lower() != "y":
            return
    # audio_filename = input("Enter audio file name: ")
    print("Transcribing audio...")
    output = requests.get(
        f"{base_url}/v1/audios/transcribe/", params={"filename": audio_filename}
    )
    message = output.json()["message"]
    print(message)


def list_audio_files():
    output = requests.get(f"{base_url}/v1/audios")
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
    output = requests.get(f"{base_url}/v1/audios")
    files = output.json()["files"]
    filename = filename.split(".")[-2] + ".wav"
    if filename in files:
        return True
    return False


def check_srt_already_exists(filename):
    output = requests.get(f"{base_url}/v1/srt/list")
    files = output.json()["files"]
    filename = filename.split(".")[-2] + ".srt"
    if filename in files:
        return True
    return False


def list_input_files():
    output = requests.get(f"{base_url}/v1/input")
    files = output.json()["files"]
    for index, file in enumerate(files):
        print(f"{index+1}. {file}")


def convert_ass_to_srt():
    output = requests.get(f"{base_url}/v1/input")
    files = output.json()["files"]
    ass_files = [f for f in files if f.endswith(".ass")]
    if not ass_files:
        print("No .ass files found.")
        return
    print("Available .ass files:")
    for index, file in enumerate(ass_files):
        print(f"{index+1}. {file}")
    try:
        choice = int(input("Enter the index of the .ass file you want to convert: "))
    except ValueError as e:
        print(e)
        return
    if choice < 1 or choice > len(ass_files):
        print("Invalid choice. Try again.")
        return
    ass_filename = ass_files[choice - 1]
    response = requests.post(
        f"{base_url}/v1/ass/to/srt", json={"ass_filename": ass_filename}
    )
    if response.status_code == 200:
        message = response.json()["message"]
        print(message)
    else:
        print("Failed to convert .ass file. Error:", response.text)


def condense_audio():
    """
    Check if it is a audio file and a srt file. Then cut the audio file based on the srt file.
    """
    audio_list = requests.get(f"{base_url}/v1/audios")
    audio_files = audio_list.json()["files"]
    srt_list = requests.get(f"{base_url}/v1/srt/list")
    srt_files = srt_list.json()["files"]
    print("Available audio files:")
    for index, file in enumerate(audio_files):
        print(f"{index+1}. {file}")
    try:
        audio_choice = int(input("Enter the index of the audio file you want to condense: "))
    except ValueError as e:
        print(e)
        return
    if audio_choice == 0 or audio_choice is None or audio_choice == "":
        return
    if audio_choice < 1 or audio_choice > len(audio_files):
        print("Invalid choice. Try again.")
        return
    
    audio_filename = audio_files[audio_choice - 1]
    print("Available SRT files:")
    for index, file in enumerate(srt_files):
        print(f"{index+1}. {file}")

    # Use os.path for proper filename handling
    base_name, _ = os.path.splitext(audio_filename)
    
    # Check for matching srt files (both simple and language-specific)
    matching_srts = []
    for srt_file in srt_files:
        srt_base, srt_ext = os.path.splitext(srt_file)
        if srt_ext == '.srt' and (srt_base == base_name or srt_base.startswith(f"{base_name}.")):
            matching_srts.append(srt_file)
    
    if matching_srts:
        if len(matching_srts) == 1:
            print(f"Found matching SRT file: {matching_srts[0]}")
            srt_filename = matching_srts[0]
        else:
            print("Found multiple matching SRT files:")
            for idx, srt in enumerate(matching_srts):
                print(f"{idx+1}. {srt}")
            try:
                choice = int(input("Select which SRT file to use (or 0 to choose from full list): "))
                if choice == 0:
                    raise ValueError
                if 1 <= choice <= len(matching_srts):
                    srt_filename = matching_srts[choice-1]
                else:
                    raise ValueError
            except ValueError:
                # Fall back to full list selection
                try:
                    srt_choice = int(input("Enter the index of the srt file you want to use: "))
                    if srt_choice < 1 or srt_choice > len(srt_files):
                        print("Invalid choice. Try again.")
                        return
                    srt_filename = srt_files[srt_choice - 1]
                except ValueError as e:
                    print(e)
                    return
    else:
        try:
            srt_choice = int(input("Enter the index of the srt file you want to use: "))
            if srt_choice < 1 or srt_choice > len(srt_files):
                print("Invalid choice. Try again.")
                return
            srt_filename = srt_files[srt_choice - 1]
        except ValueError as e:
            print(e)
            return

    print("Condensing audio...")
    payload = {"audio_filename": audio_filename, "srt_filename": srt_filename}
    result = requests.post(f"{base_url}/v1/audios/condense", json=payload)
    print(result.json())


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
