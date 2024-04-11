import io
import threading
import whisper
import logging
import os
import wave
import tempfile

import soundfile as sf
import numpy as np
import pandas as pd


from pydub import AudioSegment
from simple_diarizer.diarizer import Diarizer
from pydub.silence import split_on_silence
from df.enhance import enhance, init_df, load_audio,save_audio

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

#Loading models

# Load the diairizer model
diar = Diarizer(
    embed_model='xvec',  # 'xvec' and 'ecapa' supported
    cluster_method='sc'  # 'ahc' and 'sc' supported
)

# Load the enhancement model
model, df_state, _ = init_df() 

# Load the whisper model
whisper_model = whisper.load_model("base")



audio_path= "src/resources/test_files/"
audio_file_name = "fables_01_02_aesop.mp3"
save_path= "./"


def diarize(model,audio,sample_rate,num_speakers,threshold):
    if num_speakers is None:
        return model.diarize(audio,None, threshold)
    else:
        return model.diarize(audio, num_speakers)
    
    
def process_segment_by_speaker(segments, sample_rate):
    for segment in segments:
        start_time = segment['start']
        end_time = segment['end']
        label = segment['label']
        start_sample = int(start_time * sample_rate)
        end_sample = int(end_time * sample_rate)
        
        segment_counter = 0
        cycle_counter = 0
    
        while segment_counter < len(segments):
            cycle_counter += 1
            segment = segments[segment_counter]
            start_time = segment['start']
            current_speaker = segment['label']
            end_time = start_time

            while segment_counter < len(segments) and segments[segment_counter]['label'] == current_speaker:
                end_time = segments[segment_counter]['end']
                segment_counter += 1
            
            yield({ 'speaker': current_speaker, 'start': start_time, 'end': end_time }) 
        
def save_segments_to_files(segments_by_speaker, audio, sample_rate):
    curr_segment = 0
    for segment in segments_by_speaker:
        curr_segment += 1
        start_time = segment['start']
        end_time = segment['end']
        speaker = segment['speaker']
        start_sample = int(start_time * sample_rate)
        end_sample = int(end_time * sample_rate)
        print(f"Segment: {speaker}, Start: {start_time}, End: {end_time}, Start Sample: {start_sample}, End Sample: {end_sample}")

        segment_audio_data = audio[start_sample:end_sample]

        segment_audio_bytes = (segment_audio_data * 32767).astype(np.int16).tobytes()

        segment_audio = AudioSegment(segment_audio_bytes, 
                                     frame_rate=sample_rate,
                                     sample_width=2, 
                                     channels=2)

        file_obj = io.BytesIO()

        sf.write(file_obj, segment_audio.raw_data, sample_rate)

        file_obj.seek(0)

        yield file_obj
        
def split_until_less_than_30_seconds(file_object):
    if file_object.duration_seconds <= 30:
        file_obj = io.BytesIO()

        sf.write(file_obj, file_object.raw_data)

        file_obj.seek(0)

        yield file_obj
    else:
        half = len(file_object) // 2
        left_half = file_object[:half]
        right_half = file_object[half:]
        
        # Run each half on a new thread
        left_thread = threading.Thread(target=split_until_less_than_30_seconds, args=(left_half,))
        right_thread = threading.Thread(target=split_until_less_than_30_seconds, args=(right_half,))
        
        left_thread.start()
        right_thread.start()
        
        left_thread.join()
        right_thread.join()
        
def enhance_audio(model,df_state,audio):
    audio_file,_= load_audio(audio)
    enhanced_audio=enhance(model,df_state,audio_file)
    enhanced_audio_np = enhanced_audio.numpy()

   # Create a BytesIO object
    file_obj = io.BytesIO()

    # Convert the numpy array to 16-bit PCM
    enhanced_audio_pcm = np.int16(enhanced_audio_np * 32767).tobytes()

    # Create a wave file
    with wave.open(file_obj, 'wb') as wave_file:
        wave_file.setnchannels(1)
        wave_file.setsampwidth(2)  # 16-bit PCM
        wave_file.setframerate(sample_rate)
        wave_file.writeframes(enhanced_audio_pcm)

    file_obj.seek(0)
    return file_obj

def split_by_silence(audio):
    with io.BytesIO() as file_obj:
        sf.write(file_obj, audio.raw_data, audio.frame_rate)
        file_obj.seek(0)
        file_object = AudioSegment.from_file(file_obj, format="mp3")
        segments_silence = split_on_silence(file_object, min_silence_len=1000, silence_thresh=-60, keep_silence=250)
        for segment in segments_silence:
            file_obj = io.BytesIO()

            sf.write(file_obj, segment.export(f"segment_{segments_silence.index(segment)}.wav", format="wav").raw_data)

            file_obj.seek(0)

            yield file_obj

def transcribe(whisper_model,audio):
    return whisper.transcribe(whisper_model, audio)
    

        
# Start the transcription process

# Load the audio file
audio_file_path=os.path.join(audio_path,audio_file_name)
audio_file,_= load_audio(audio_file_path)
audio, sample_rate = sf.read(audio_file_path)
logging.info(f"Loaded audio with {len(audio)} samples at {sample_rate} Hz")

enhanced_audio=enhance_audio(model,df_state,audio_file_path)
logging.info(f"Enhanced audio at {sample_rate} Hz")

enhanced_audio_tempfile = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
enhanced_audio_tempfile.write(enhanced_audio.read())
logging.info(f"Saved enhanced audio to temporary file: {enhanced_audio_tempfile.name}")

diarized_segments=diarize(diar,enhanced_audio_tempfile.name,sample_rate,num_speakers=None,threshold=0.2)
logging.info(f"Diarized audio with {len(diarized_segments)} segments")

segments_by_speaker=list(process_segment_by_speaker(diarized_segments,sample_rate))
logging.info("Processed segments by speaker")

files_by_speaker=list(save_segments_to_files(segments_by_speaker, audio, sample_rate))
logging.info("Saved segments to files")

segments_silent=[]
for segment in files_by_speaker:
    segments_silent.append(list(split_by_silence(segment)))
    logging.info("Split segments by silence")

segments_split_by_30_seconds=[]
for segment in segments_silent:
    segments_split_by_30_seconds.append(list(split_until_less_than_30_seconds(segment)))
    logging.info("Split segments by 30 seconds segments")


transcriptions=[]

for segment in segments_split_by_30_seconds:
    transcriptions.append(transcribe(whisper_model,segment))
    logging.info("Transcribed segment")
   
for transcription in transcriptions:
    print(transcription['text'])



        
        
