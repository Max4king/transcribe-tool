#!/bin/bash

BASE_URL="http://0.0.0.0:5000"

# Function to check if the server is running
check_server() {
    for i in {1..3}; do
        response=$(curl -s -o /dev/null -w "%{http_code}" $BASE_URL)
        if [ "$response" -eq 200 ]; then
            echo "Server is running."
            return 0
        else
            echo "Server is not running. Attempting to wait for the server..."
            sleep 1
        fi
    done
    echo "Failed to connect to the server after 3 attempts."
    read -p "Do you wish to force start the server? (y/N): " choice
    if [[ "$choice" =~ ^[Yy]$ ]]; then
        docker compose up -d
        return 0
    else
        exit 1
    fi
}
# 

# Function to transcribe audio
transcribe_audio() {
    local file_path=$1
    local filename=$(basename -- "$file_path")
    local extension="${filename##*.}"
    local filename_without_ext="${filename%.*}"

    # Check if SRT file already exists
    response=$(curl -s "$BASE_URL/v1/srt/list")
    if echo "$response" | grep -q "\"$filename_without_ext.srt\""; then
        echo "SRT file already exists for this audio."
        read -p "Do you want to transcribe again? (y/N): " choice
        if [[ ! "$choice" =~ ^[Yy]$ ]]; then
            return
        fi
    fi

    echo "Transcribing audio..."
    response=$(curl -s -G "$BASE_URL/v1/audios/transcribe/" --data-urlencode "filename=$filename")
    message=$(echo "$response" | jq -r '.message')
    echo "$message"
}

# Main script   
if [ $# -ne 1 ]; then
    echo "Usage: $0 <file_path>"
    exit 1
fi

file_path=$1

check_server
transcribe_audio "$file_path"