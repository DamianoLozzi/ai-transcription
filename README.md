# Project Documentation
## Overview
This project is designed to provide audio processing capabilities, including audio enhancement, diarization, segmentation, and transcription. It leverages various Python libraries and pretrained models to process audio files, making it suitable for applications requiring audio analysis and transcription services.

## Features
 
 - **Audio Enhancement**: Improves the quality of audio files by reducing noise and enhancing clarity.
 - **Diarization**: Identifies different speakers in an audio file, useful for processing interviews, meetings, and multi-speaker recordings.
 - **Audio Segmentation**: Splits audio files into smaller segments based on silence detection, facilitating easier processing and analysis.
 - **Transcription**: Converts speech in audio files to text, supporting both single-speaker and multi-speaker audio files.

## Installation
To set up the project,  you can either run the **run.sh** script or follow the steps below:

1. Clone the repository:

```bash
git clone https://github.com/DamianoLozzi/transcription-service.git
```

2. Install the required packages:

```bash
pip install -r requirements.txt
```


## Usage
The project is structured as a Flask web application, providing endpoints for audio enhancement and transcription.

## Starting the Server

Run the following command to start gunicon server

```bash
gunicorn --config gunicorn_config.py app:app
```

Alternatively, you can run the docker container by executing the following commands:

```bash
docker build -t transcription-service .
docker run -p 5000:5000 transcription-service # Replace 5000 with the desired port
```

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

or

```bash
curl -X POST -F 'file=@path/to/your/audio/file' -F 'threshold=0.5' http://localhost:5000/transcribe
```

Replace path/to/your/audio/file with the actual path to your audio file and adjust the speakers/threshold parameter as needed.