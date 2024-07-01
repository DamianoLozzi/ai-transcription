#!/bin/bash

# update the package list
sudo apt update


# if ffmpeg is not installed, install it
if ! [ -x "$(command -v ffmpeg)" ]; then
    echo "Installing ffmpeg"
    sudo apt install ffmpeg -y
fi

# if python3 is not installed, install it
if ! [ -x "$(command -v python3)" ]; then
    echo "Installing python3"
    sudo apt install python3 -y
fi

# if python3-venv is not installed, install it
if ! [ -x "$(command -v python3-venv)" ]; then
    echo "Installing python3-venv"
    sudo apt install python3-venv -y
fi

# if pip is not installed, install it
if ! [ -x "$(command -v pip)" ]; then
    echo "Installing pip"
    sudo apt install python3-pip -y
fi

# if git is not installed, install it
if ! [ -x "$(command -v git)" ]; then
    echo "Installing git"
    sudo apt install git -y
fi

# create a virtual environment if it does not exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment"
    python3 -m venv venv && echo "Virtual environment created" || echo "Failed to create virtual environment"
fi

# activate the virtual environment
source venv/bin/activate && echo "Virtual environment activated" || echo "Failed to activate virtual environment"

# install requirements if not already installed
if [ ! -f ".install_done" ]; then
    echo "Installing requirements"
    pip install -r requirements.txt && touch .install_done && echo "Requirements installed" || echo "Failed to install requirements"
fi

# run the flask app
flask run