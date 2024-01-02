#!/bin/bash

echo "Starting installation"
#verifies that install_done file does not exist
if [ -f .install_done ]; then
    echo "Installation has already been done. If you want to reinstall, please delete the install_done file"
    
else
    echo "Installation has not been done. Proceeding with installation"

# Install dependencies
sudo apt update
sudo apt install ffmpeg libespeak-ng1

# creates a directory for the models
mkdir models
# downloads the llama model into the models directory
wget https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF/resolve/main/llama-2-7b-chat.Q2_K.gguf?download=true -P models

# Create python venv
python3 -m venv venv
source venv/bin/activate

# Install python dependencies
#stt 
pip install git+https://github.com/openai/whisper.git 
#tts
pip install git+https://github.com/suno-ai/bark.git
pip install ipython
pip install -r requirements.txt



# Creates an install_done file to indicate that the installation is complete
touch .install_done
fi

# activates the python venv
source venv/bin/activate

# starts the server
flask run 
