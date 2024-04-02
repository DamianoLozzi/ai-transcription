#!/bin/bash

# Create a virtual environment if not present

if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

source ./venv/bin/activate

export PYTHONPATH=$PYTHONPATH:$(pwd)/src

# if .install_done file is not present,Install requirements
if [ ! -f ".install_done" ]; then
    sudo apt-get update
    sudo apt-get install -y python3 python3-venv python3-pip ffmpeg
    pip install -r requirements.txt
    source ./venv/bin/activate
    touch .install_done
fi

source ./venv/bin/activate

# Run all test files that start with "test_"
pytest -v src/test_*

# If the tests pass, run the app
if [ $? -eq 0 ]; then
    export FLASK_APP=transcribe.py
    # Run the application
    flask run
else
    echo "Tests failed, not starting the app."
fi