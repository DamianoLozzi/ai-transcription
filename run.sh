#!/bin/bash

arg1=$1

if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

source ./venv/bin/activate


# if .install_done file is not present,Install requirements
if [ ! -f ".install_done" ]; then
    sudo apt-get update
    sudo apt-get install -y python3 python3-venv python3-pip ffmpeg
    pip install -r requirements.txt
    # Create a virtual environment if not present
 

    # Check if installation was successful
    if [ $? -eq 0 ]; then
        echo "Installation successful."
        touch .install_done
    else
        echo "Installation failed."
        exit 1
    fi
    else
    echo "Requirements already installed."
fi

# Create a virtual environment if not present
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi
# Activate the virtual environment
echo "Activating virtual environment..."
source ./venv/bin/activate
# Add the src directory to the PYTHONPATH
echo "Adding src directory to PYTHONPATH..."
export PYTHONPATH=$PYTHONPATH:$(pwd)/src

# Run all test files that start with "test_" if arg1 not "--skipTests"
if [ "$arg1" != "--skipTests" ]; then
    echo "Running tests..."
    pytest  -n auto -v src/test_*
    else 
    echo "Skipping tests..."
fi

# If the tests pass, run the app
if [ $? -eq 0 ]; then
    echo "Tests passed, starting the app..."
    export FLASK_APP=transcribe.py
    # Run the application
    flask run
else
    echo "Tests failed, not starting the app."
fi