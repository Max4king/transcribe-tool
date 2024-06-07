#!/bin/bash

# Check if the image is already built
if [ ! -f dockerbuilt ]; then
    # Build the image from the Dockerfile
    docker build -t transcribe_server .
    touch dockerbuilt
else
    echo "Image already built"
fi
# Run a container from the image
konsole --noclose  -e "docker compose up" &

# Run the server
if [ ! -d venv ]; then
    python3 -m venv venv
else
    echo "Virtual environment already created"
fi

source venv/bin/activate

python main.py

docker compose down