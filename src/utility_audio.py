import librosa
import pathlib
from pydub import AudioSegment
from pydub.utils import make_chunks

def audio_length(audio_file):
    audio, sr = librosa.load(audio_file)
    return librosa.get_duration(y=audio, sr=sr)

def split_in_chunks(audio_file, chunk_length):
    audio= AudioSegment.from_file(audio_file)
    chunks = make_chunks(audio, chunk_length*1000)
    return chunks

def process_long_audio(audio_file, chunk_length_ms):
    audio_name = pathlib.Path(audio_file).stem
    audio_suffix = pathlib.Path(audio_file).suffix[1:]
    myaudio = AudioSegment.from_file(audio_file, audio_suffix)
    chunks = make_chunks(myaudio,chunk_length_ms) 
    files=[]
    for i, chunk in enumerate(chunks): 
        chunk_name = f"{0}.{audio_suffix}".format(i) 
        print ("exporting", chunk_name) 
        chunk.export(chunk_name, format="wav")
        lm.log('info', f"Saved chunk to temporary file: {audio_name}{audio_suffix}")
        files.append(chunk_name)
    return files