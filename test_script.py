import os
import pandas as pd

from pydub import AudioSegment
from pydub.silence import split_on_silence
from df.enhance import enhance, init_df, load_audio,save_audio
from pyAudioAnalysis import audioSegmentation as aS
import threading


audio_path= "src/resources/test_files/"
audio_file = "fables_01_02_aesop.mp3"
save_path= "./"


def split_until_less_than_30_seconds(file_object):
    if file_object.duration_seconds <= 30:
        segments.append(file_object)
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

        # Rest of the code...

model, df_state, _ = init_df() 
print("model loaded")
audio_file,_= load_audio(audio_path+audio_file)
print("audio loaded")
enhanced_audio=enhance(model,df_state,audio_file)
save_audio(save_path+"enhanced.wav", enhanced_audio, df_state.sr())
print("audio enhanced")
# speaker diarization
speaker_labels_tuple = aS.speaker_diarization(save_path+"enhanced.wav", n_speakers=0, mid_window=2.0, mid_step=0.2, short_window=0.05, lda_dim=0)

diarize_df = pd.DataFrame(speaker_labels_tuple, columns=["start", "end", "speaker"])

print(diarize_df)


file_object = AudioSegment.from_file(save_path+"enhanced.wav", format="mp3")
print("file object created")
#reduce background noise
print(f"Duration: {file_object.duration_seconds}")
print(f"Frame rate: {file_object.frame_rate}")
print(f"Channels: {file_object.channels}")

# split the file in half until the duration of each segment is less than 30 seconds
segments = []
segments_silence = split_on_silence(file_object, min_silence_len=1000, silence_thresh=-60, keep_silence=250)

        
for segment in segments_silence:
    segment.export(f"segment_{segments_silence.index(segment)}.wav", format="wav")
    # export into a file object
    print(f"Segment not silent duration: {segment.duration_seconds}")        
    
for segment in segments:
    print(f"Segment duration: {segment.duration_seconds}")
    
    

