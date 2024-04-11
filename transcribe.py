import os
import threading
import tempfile
from flask import Flask, request, jsonify
from pydub import AudioSegment
import whisper
import queue
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/transcribe', methods=['POST'])
def transcribe():
    # load the model
    model = whisper.load_model("base")
    # get the file
    file = request.files['file']
    # split the file into 30 second chunks
    audio = AudioSegment.from_file(file)
    # Define the chunk length in milliseconds
    chunk_length_ms = 30*1000
    # Break down the audio file into chunks
    chunks = [audio[i:i + chunk_length_ms] for i in range(0, len(audio), chunk_length_ms)]
    # Queue to hold chunks
    chunk_queue = queue.Queue()
    # Initialize the queue with chunks
    for chunk in chunks:
        chunk_queue.put(chunk)
    # Initialize transcriptions list
    transcriptions = []

    # Function to transcribe a chunk
    def transcribe_chunk():
        while not chunk_queue.empty():
            chunk = chunk_queue.get()
            # Create a temporary file to save the chunk
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_file:
                temp_file_path = temp_file.name
                chunk.export(temp_file_path, format="mp3")
                logger.info(f"Saved chunk to temporary file: {temp_file_path}")

                # Transcribe the chunk
                logger.info(f"Transcribing chunk from temporary file: {temp_file_path}")
                transcription = whisper.transcribe(model, temp_file_path)
                text = transcription['text']
                logger.info(f"Transcription for chunk: {text}")

                # Remove the temporary file
                os.remove(temp_file_path)

                # Append transcription to the list
                transcriptions.append(text)

    # Start transcription of first chunk immediately
    logger.info("Starting transcription...")
    transcribe_thread = threading.Thread(target=transcribe_chunk)
    transcribe_thread.start()
    transcribe_thread.join()

    # Combine the transcriptions
    transcribed = " ".join(transcriptions)

    # Return the transcribed text
    logger.info("Transcription completed.")
    return jsonify({"transcription": transcribed})

if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=5000)
