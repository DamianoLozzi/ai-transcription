from flask import Flask, abort, request
from tempfile import NamedTemporaryFile
import scipy
import src.TtsModel as tts 
import src.LlamaModel as llama
import src.WhisperModel as whisper

app = Flask(__name__)

@app.route('/transcribe', methods=['POST'])
def transcribe_request():
    if not request.files:
        abort(400)

    results = []

    for filename, handle in request.files.items():
        temp = NamedTemporaryFile()
        handle.save(temp)
        result = whisper.transcribe_file(temp.name)
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
        result = transcribe_file(temp.name)
        instruction="###Instruction:" + result['text'] + "###Response:"
        output = LlamaModel.get_instance()(instruction)
        audio = TtsModel.get_instance()[1].generate(TtsModel.get_instance()[0](output["choices"][0]["text"], return_tensors="pt"))
        wav = "this is a wav" # scipy.io.wavfile.write("bark_out.wav", rate=TtsModel.get_instance()[2], data=audio.cpu().numpy().squeeze())
    
        
        results.append({
            'transcript': result['text'],
            'output': output["choices"][0]["text"],
            'audio': wav
        })

    # This will be automatically converted to JSON.
    return {'results': results}

