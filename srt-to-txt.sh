#!/bin/bash

# Check if the input file is provided
if [ -z "$1" ]; then
    echo "Please provide the input .srt file as an argument."
    exit 1
fi

# Check if the input file exists
if [ ! -f "$1" ]; then
    echo "Input file does not exist."
    exit 1
fi

# Get the filename without extension
filename=$(basename "$1")
filename="${filename%.*}"

# Convert .srt to .txt
sed -e '/^[0-9]*$/d' -e '/^[0-9]*:[0-9]*:[0-9]*,[0-9]* --> [0-9]*:[0-9]*:[0-9]*,[0-9]*$/d' -e '/^$/d' "$1" > "$filename.txt"

echo "Conversion complete. Output file: $filename.txt"