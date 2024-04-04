import librosa
import pathlib
from pydub import AudioSegment
from pydub.utils import make_chunks
from utility_log import LogManager as lm

def audio_length(audio_file):
    audio, sr = librosa.load(audio_file)
    return librosa.get_duration(y=audio, sr=sr)

def split_in_chunks(audio_segment, chunk_length_ms=30 * 1000, index=0):
    # Base case: If the audio segment is shorter than 30 seconds, export it and return
    if len(audio_segment) <= chunk_length_ms:
        audio_segment.export(f"chunk_{index}.wav", format="wav")
        return

    # Calculate the midpoint of the audio segment
    midpoint = len(audio_segment) // 2

    # Split the audio segment into two halves
    left_half = audio_segment[:midpoint]
    right_half = audio_segment[midpoint:]

    # Recursively split each half
    split_in_chunks(left_half, chunk_length_ms, index)
    split_in_chunks(right_half, chunk_length_ms, index + len(left_half) // chunk_length_ms)

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
        os.remove(chunk_name)
    return files