from flask import Flask, request, send_file, stream_with_context, Response
from audio_processing import Diarization, AudioEnhancement, Transcription, AudioSegmentation
import tempfile
import os
from threading import Lock
import traceback
import text_generation as tg
import custom_logger as log
import json

audio_enhancement = AudioEnhancement()
aus = AudioSegmentation()
transcriber = Transcription("auto")
transcribe_lock = Lock()
enhance_lock = Lock()
generate_lock = Lock()

app = Flask(__name__)
log.info("Started Flask app")

@app.route('/enhance', methods=['POST'])
def _enhance():
    try:
        log.info("Received request to enhance audio")
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
    except Exception as e:
        log.error(f"An error occurred during audio enhancement: {e}")
        return str(e), 400

@app.route('/transcribe', methods=['POST'])
def _transcribe():
    log.info("Received request to transcribe audio")
    def generate():
        if 'file' not in request.files:
            yield json.dumps({'error': 'No file part'}).encode('utf-8')
            return
        if 'speakers' not in request.form:
            yield json.dumps({'error': 'No speakers part'}).encode('utf-8')
            return
        try:
            file = request.files['file']
            file_extension = file.filename.split('.')[-1]
            speakers = int(request.form['speakers'])
            for segment in transcribe(file, file_extension, speakers):
                yield segment
        except Exception as e:
            log.error(f"An error occurred during transcription: {e}")
            yield json.dumps({'error': str(e)}).encode('utf-8')
        finally:
            file.close()
    return Response(stream_with_context(generate()), content_type='application/json; charset=utf-8')

def transcribe(file, suffix, speakers):
    try:
        temp_file = tempfile.NamedTemporaryFile(delete=True, suffix='.' + suffix)
        file_content = file.read()
        temp_file.write(file_content)
        temp_file.flush()
        temp_file_path = temp_file.name
        # Transcribe
        transcriptions = []
        
        diarization = Diarization(embed_model='xvec', cluster_method='sc')
        diarization.load(temp_file_path, num_speakers=speakers)
        segments_by_speaker = diarization.segment_audio_by_speaker()
        for segment_info in diarization.save_segments_to_files(segments_by_speaker):
            speaker = segment_info['speaker']
            file_path = segment_info['file_path']
            yield json.dumps({"speaker": int(speaker)}, ensure_ascii=False).encode("utf-8")
            with transcribe_lock:
                transcription = transcriber.transcribe(file_path)
            yield json.dumps({"text": transcription['text']}, ensure_ascii=False).encode("utf-8")
            transcriptions.append({"speaker": speaker, "text": transcription['text']})
        with generate_lock:
            summary = tg.generate_summary(transcriptions)
            yield json.dumps({"summary": summary}, ensure_ascii=False).encode("utf-8")
            title = tg.generate_name(summary, "title")
            yield json.dumps({"title": title}, ensure_ascii=False).encode("utf-8")
    except Exception as e:
        log.error(f"An error occurred during transcription: {e}")
        log.error(traceback.format_exc())
        yield json.dumps({'error': str(e)}, ensure_ascii=False).encode('utf-8')
    finally:
        temp_file.close()

def enhance(file):
    try:
        temp_file = tempfile.NamedTemporaryFile(delete=True)
        file_content = file.read()
        temp_file.write(file_content)
        temp_file.flush()
        temp_file_path = temp_file.name
        with enhance_lock:
            enhanced_file_path = audio_enhancement.enhance_and_save_as_temp_file(temp_file_path)
        temp_file.close()
        log.info(f"Audio enhancement complete: {enhanced_file_path}")
        return enhanced_file_path
    except Exception as e:
        log.error(f"An error occurred during audio enhancement: {e}")
        return str(e), 500

if __name__ == '__main__':
    app.run(debug=True)
