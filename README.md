# Transcribe-tool

My collection of program that I found and made for transcribing audio to text. It is probably an over complicated way of transcribing an audio but it works.

## Requirements

1. Python 3.12.X (Other version may work but it is not tested.)
2. Docker setup


## Installation


Clone this repository.
```
git https://github.com/Max4king/transcribe-tool.git
```
Build the image. (Always build a new one whenever you change something in the Dockerfile or server.py)

```
docker build -t transcribe_server .
```


## Usage

### Method 1 (Manually. For most stable experience.) Recommended

Run the docker image to start the server.

```
docker compose up
```
Start the program. (This is basically a cli frontend. You could replace it with your own or I may build other interface later on.)
```
python main.py
```

### Mehtod 2 (Start script) Linux only. Only if believe in my scripting skill or know one.

The easiest way to run it for now. 
```
./start.sh
```
That is it. It just runs the build command and start the server and interface like method 1. But it is done in one step.