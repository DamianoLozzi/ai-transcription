#!/bin/bash

echo "Starting installation"
#verifies that install_done file does not exist
if [ -f .install_done ]; then
    echo "Installation has already been done. If you want to reinstall, please delete the install_done file"
    
else
    echo "Installation has not been done. Proceeding with installation"

# Install dependencies
sudo apt update
sudo apt install ffmpeg libespeak-ng1 python3.11-venv python3.11-dev python3-pip -y

# creates a directory for the models
mkdir models
# downloads the llama model into the models directory if not already downloaded
if [ -f models/llama-2-7b-chat.Q2_K.gguf ]; then
    echo "Llama model already downloaded"
else
    echo "Downloading Llama model"
#wget https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF/resolve/main/llama-2-7b-chat.Q2_K.gguf?download=true -P models
fi 
# https://huggingface.co/TheBloke/llama2_7b_chat_uncensored-GGUF/resolve/main/llama2_7b_chat_uncensored.Q8_0.gguf

if [ -f models/llama2_7b_chat_uncensored.Q8_0.gguf ]; then
    echo "Llama model already downloaded"
else
    echo "Downloading Llama model" 
#wget https://huggingface.co/TheBloke/llama2_7b_chat_uncensored-GGUF/resolve/main/llama2_7b_chat_uncensored.Q8_0.gguf -P models
fi

# Create python venv
python3 -m venv venv
source venv/bin/activate

# Install python dependencies
#stt 
pip install git+https://github.com/openai/whisper.git 
#tts
pip install git+https://github.com/suno-ai/bark.git
pip install -r requirements.txt

# Creates an install_done file to indicate that the installation is complete
touch .install_done
fi

# activates the python venv
source venv/bin/activate

# starts the server
flask run 
