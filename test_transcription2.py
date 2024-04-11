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
from pydub.utils import mediainfo
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

# Load the audio file
audio_file,sample_rate= load_audio(audio_path+audio_file_name)
logging.log(logging.INFO, "audio loaded")

# Enhance the audio
enhanced_audio=enhance(model,df_state,audio_file)
logging.log(logging.INFO, "audio enhanced")


# Save the enhanced audio
save_audio(save_path+"enhanced.wav", enhanced_audio, df_state.sr())
logging.log(logging.INFO, "audio saved")

info = mediainfo(save_path+"enhanced.wav")
sample_rate = int(info['sample_rate'])
# Load the enhanced audio file
file_object = AudioSegment.from_file(save_path+"enhanced.wav", format="mp3")
logging.log(logging.INFO, "file object created")

# diarize the audio

diarized = diar.diarize(save_path+"enhanced.wav", None, 0.5)
logging.log(logging.INFO, "audio diarized")

segments_by_speaker = []

# Split the audio into segments
for segment in diarized:
    start_time = segment['start']
    end_time = segment['end']
    label = segment['label']
    start_sample = int(start_time * df_state.sr())
    end_sample = int(end_time * df_state.sr())
    
    segment_counter = 0
    cycle_counter = 0

    while segment_counter < len(diarized):
        cycle_counter += 1
        segment = diarized[segment_counter]
        start_time = segment['start']
        current_speaker = segment['label']
        end_time = start_time

        while segment_counter < len(diarized) and diarized[segment_counter]['label'] == current_speaker:
            end_time = diarized[segment_counter]['end']
            segment_counter += 1
        segments_by_speaker.append({ 'speaker': current_speaker, 'start': start_time, 'end': end_time })

files_by_speaker = []

curr_segment = 0
for segment in segments_by_speaker:
    curr_segment += 1
    start_time = segment['start']
    end_time = segment['end']
    speaker = segment['speaker']
    start_sample = int(start_time * sample_rate)
    end_sample = int(end_time * sample_rate)
    print(f"Segment: {speaker}, Start: {start_time}, End: {end_time}, Start Sample: {start_sample}, End Sample: {end_sample}")

    # Save the segment to a file
    segment_audio = file_object[start_sample:end_sample]
    segment_audio.export(f"{save_path}{audio_file_name}_{curr_segment}_{speaker}.wav", format="wav")
    files_by_speaker.append(f"{save_path}{audio_file_name}_{curr_segment}_{speaker}.wav")
    
# Split each segment by silence

files_by_speaker_silence = []
for file in files_by_speaker:
    file_object = AudioSegment.from_file(file, format="wav")
    segments_silence = split_on_silence(file_object, min_silence_len=1000, silence_thresh=-60, keep_silence=250)
    segments = []
    for segment in segments_silence:
        segment.export(f"{file.split('.')[0]}_segment_{segments_silence.index(segment)}.wav", format="wav")
        segments.append(f"{file.split('.')[0]}_segment_{segments_silence.index(segment)}.wav")
        files_by_speaker_silence.append(segments)

# Transcribe each segment
for file in files_by_speaker_silence:
    audio, sample_rate = sf.read(file)
    print(f"Loaded audio with {len(audio)} samples at {sample_rate} Hz")
    transcribed_segment=whisper.transcribe(whisper_model, audio)
    print(f"Transcribed segment: {transcribed_segment['text']}")
    
    