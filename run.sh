#!/bin/bash

if [ ! -d "venv" ]; then
    echo "Creating virtual environment"
    python3 -m venv venv && echo "Virtual environment created" || echo "Failed to create virtual environment"
fi

source venv/bin/activate && echo "Virtual environment activated" || echo "Failed to activate virtual environment"

if [ ! -f ".install_done" ]; then
    echo "Installing requirements"
    pip install -r requirements.txt && touch .install_done && echo "Requirements installed" || echo "Failed to install requirements"
fi

flask run