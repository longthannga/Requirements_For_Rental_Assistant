#!/bin/bash

DATE=$(date +'%Y-%m-%d')
FILE_PATH="./src/phrases/$DATE.md"
MODEL='gemma3:4b-motivational'
MODEL_FILE='./Modelfile'

# Avoid running the command if the file already exists
if [ -f "$FILE_PATH" ]; then
    echo '[INFO] Phrase already exists, skipping...'
    exit 1
fi

echo '[INFO] Creating new model based on Modelfile...'
ollama create $MODEL -f $MODEL_FILE
