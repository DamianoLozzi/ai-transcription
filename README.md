# Project Documentation
## Overview
This project is designed to provide audio processing capabilities, including audio enhancement, diarization, segmentation, and transcription. It leverages various Python libraries and pretrained models to process audio files, making it suitable for applications requiring audio analysis and transcription services.

## Features
 
 - **Audio Enhancement**: Improves the quality of audio files by reducing noise and enhancing clarity.
 - **Diarization**: Identifies different speakers in an audio file, useful for processing interviews, meetings, and multi-speaker recordings.
 - **Audio Segmentation**: Splits audio files into smaller segments based on silence detection, facilitating easier processing and analysis.
 - **Transcription**: Converts speech in audio files to text, supporting both single-speaker and multi-speaker audio files.

## Installation
To set up the project, ensure you have Python installed on your system. Then, follow these steps:

 1. Clone the repository to your local machine.
 2. Install the required Python packages by running:
```bash
pip install -r requirements.txt
```
 3. Download and place the pretrained models in the pretrained_models/spkrec-xvect-voxceleb/ directory.

## Usage
The project is structured as a Flask web application, providing endpoints for audio enhancement and transcription.

## Starting the Server
Run the Flask application by executing:

```bash
flask run
```

This will start the server on localhost with the default port 5000.

## Endpoints

 - Audio Enhancement

>POST /enhance

Enhances the quality of an uploaded audio file.

 - Transcription

Example Request
To enhance an audio file, you can use the following curl command:

```bash
curl -X POST -F 'file=@path/to/your/audio/file' http://localhost:5000/enhance
```

>POST /transcribe

Transcribes the speech in an uploaded audio file. This endpoint accepts an audio file and the number of speakers as input and returns the transcription.

Example Request
To transcribe an audio file with multiple speakers, you can use the following curl command:

```bash
curl -X POST -F 'file=@path/to/your/audio/file' -F 'speakers=2' http://localhost:5000/transcribe
```

Replace path/to/your/audio/file with the actual path to your audio file and adjust the speakers parameter as needed.

---

**Contributing**
Contributions to this project are welcome. Please ensure you follow the coding standards and write tests for new features.

**License**
This project is licensed under the MIT License - see the LICENSE file for details.

This README provides a basic overview and setup instructions for the project. For detailed documentation on the implementation and usage of each feature, refer to the source code and comments within the app.py and audio_processing.py files.