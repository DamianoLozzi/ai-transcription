from flask import Flask, request, send_file
from audio_processing import Diarization,AudioEnhancement, Transcription, AudioSegmentation
import numpy as np
import tempfile
import os
from threading import Lock
import custom_logger as logging 
import traceback
import text_generation as tg
import custom_logger as log


audio_enhancement = AudioEnhancement()
aus=AudioSegmentation()
transcriber=Transcription("tiny")
transcribe_lock = Lock()
enhance_lock = Lock()

app = Flask(__name__)


@app.route('/enhance', methods=['POST'])
def _enhance():
    if 'file' not in request.files:
        return 'No file part', 400
    file = request.files['file']
    temp_dir = tempfile.mkdtemp()
    temp_path = os.path.join(temp_dir, file.filename)
    file.save(temp_path)
    with enhance_lock:
        enhanced_file_path = audio_enhancement.enhance_and_save_as_temp_file(temp_path)
    os.remove(temp_path)
    os.rmdir(temp_dir)
    return send_file(enhanced_file_path, as_attachment=True)
    
@app.route('/transcribe', methods=['POST'])
def _transcribe():
    if 'file' not in request.files:
        return 'No file part', 400
    if 'speakers' not in request.form:
        return 'No speakers part', 400
    try:
        file = request.files['file']
        file_extension = file.filename.split('.')[-1]
        speakers = int(request.form['speakers'])
        return transcribe(file,file_extension,speakers)
    except Exception as e:
        return str(e), 400
    finally:
        file.close()

def transcribe(file,suffix,speakers):
    try:
        temp_file = tempfile.NamedTemporaryFile(delete=True,suffix='.'+suffix)
        file_content = file.read()  
        temp_file.write(file_content)
        temp_file.flush()  
        temp_file_path = temp_file.name
        # Transcribe
        transcriptions = []
        if speakers == 1:
            text = []
            print("Transcribing file:", temp_file_path)
            for segment in aus.split_on_silence(file_path=temp_file_path):
                logging.debug(f"Transcribing segment: {segment}")
                with transcribe_lock:
                    text.append(transcriber.transcribe(segment)['text'])
            transcriptions.append({"speaker": "0", "text": " ".join(text)})
        else :
            diarization = Diarization(embed_model='xvec', cluster_method='sc')
            diarization.load(temp_file_path, num_speakers=speakers)  
            segments_by_speaker = diarization.segment_audio_by_speaker()
            for segment_info in diarization.save_segments_to_files(segments_by_speaker):
                speaker=segment_info['speaker']
                file_path=segment_info['file_path']
                print("Transcribing file:", file_path)
                print("Speaker:", speaker)
                with transcribe_lock:
                    transcription = transcriber.transcribe(file_path)
                transcriptions.append({"speaker": str(speaker), "text": transcription['text']})
        title = tg.generate_name(transcriptions[0]['text'],"title")
        log.critical("filename: "+tg.generate_name(transcriptions[0]['text'],"filename"))
        return {"title": title, "transcriptions": transcriptions}
    except Exception as e:
        logging.error(f"An error occurred during transcription: {e}")
        logging.error(traceback.format_exc())
        return str(e), 500
    finally:
        temp_file.close()
        
def enhance(file):
    temp_file = tempfile.NamedTemporaryFile(delete=True)
    file_content = file.read()  
    temp_file.write(file_content)
    temp_file.flush()  
    temp_file_path = temp_file.name
    with enhance_lock:
        enhanced_file_path = audio_enhancement.enhance_and_save_as_temp_file(temp_file_path)
    temp_file.close()
    return enhanced_file_path
    
