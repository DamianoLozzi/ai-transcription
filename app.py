from flask import Flask, abort, request
from tempfile import NamedTemporaryFile
import scipy
from TtsModel import TtsModel
from LlamaModel import LlamaModel
from WhisperModel import WhisperModel
import threading

app = Flask(__name__)

whisperModel = WhisperModel()
llamaModel = LlamaModel()
ttsModel = TtsModel()



@app.route('/transcribe', methods=['POST'])
def transcribe_request():
    if not request.files:
        abort(400)

    results = []

    for filename, handle in request.files.items():
        temp = NamedTemporaryFile()
        handle.save(temp)
        result = whisperModel.transcribe_file(temp.name)
        results.append({
            'transcript': result['text']
        })

    return {'results': results}

@app.route('/generate', methods=['POST'])
def generate_request():
    if not request.files:
        abort(400)

    results = []

    for filename, handle in request.files.items():
        temp = NamedTemporaryFile()
        handle.save(temp)
        result = whisperModel.transcribe_file(temp.name)
        instruction="###Instruction:" + result['text'] + "###Response:"
        output = llamaModel.generate(instruction)
        audio = ttsModel.speak(output["choices"][0]["text"])
        wav = scipy.io.wavfile.write("bark_out.wav", rate=ttsModel.SAMPLE_RATE, data=audio.squeeze())
    
        
        results.append({
            'transcript': result['text'],
            'output': output["choices"][0]["text"],
            'audio': wav
        })

    # This will be automatically converted to JSON.
    return {'results': results}

