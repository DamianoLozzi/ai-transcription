from resemblyzer import preprocess_wav
from pydub import AudioSegment
import numpy as np
import soundfile as sf
import io
from simple_diarizer.diarizer import Diarizer
import os
from concurrent.futures import ThreadPoolExecutor
import threading

num_cores = os.cpu_count()
MAX_CONCURRENT_THREADS = max(1, num_cores - 1)
best_threshold_lock = threading.Lock()
best_accuracy_lock = threading.Lock()


best_threshold_lock = threading.Lock()
best_accuracy_lock = threading.Lock()
best_threshold = 1000
best_accuracy = 1000

def diarize(AUDIO_FILE, THRESHOLD, EXPECTED_SPEAKERS):
    FILE_NAME = AUDIO_FILE.split('/')[-1].split('.')[0]

    diar = Diarizer(
        embed_model='xvec',  # 'xvec' and 'ecapa' supported
        cluster_method='sc'  # 'ahc' and 'sc' supported
    )
    segments = diar.diarize(AUDIO_FILE, num_speakers=None, threshold=THRESHOLD)

    # Load the audio file
    audio, sample_rate = sf.read(AUDIO_FILE)
    print(f"Loaded audio with {len(audio)} samples at {sample_rate} Hz")

    # Process each segment
    for segment in segments:
        start_time = segment['start']
        end_time = segment['end']
        label = segment['label']
        start_sample = int(start_time * sample_rate)
        end_sample = int(end_time * sample_rate)
        
        print(f"Segment: {label}, Start: {start_time}, End: {end_time}, Start Sample: {start_sample}, End Sample: {end_sample}")

        
    # Extract speaker IDs
    speaker_ids = set(segment["label"] for segment in segments)

    # Count the total number of speakers
    total_speakers = len(speaker_ids)

    print("Total number of speakers:", total_speakers)
    return total_speakers
    
    
def test_accuracy(AUDIO_FILE, THRESHOLD, EXPECTED_SPEAKERS):
    total_speakers = diarize(AUDIO_FILE, THRESHOLD, EXPECTED_SPEAKERS)
    return abs(total_speakers - EXPECTED_SPEAKERS)


files_to_test_with_expected_speakers = [['src/resources/test_files/LE_listening_A2_Changing_a_meeting_time.mp3', 3],
                                        ['src/resources/test_files/LE_listening_A2_An_invitation_to_a_party.mp3', 3],
                                        ['src/resources/test_files/test_long.wav', 8]]



# Function to test a single threshold
def test_threshold(file, expected_speakers, threshold):
    accuracy = test_accuracy(file, threshold, expected_speakers)
    with best_accuracy_lock:
        global best_accuracy, best_threshold
        if accuracy < best_accuracy:
            best_accuracy = accuracy
            best_threshold = threshold
            
# Function to process each file with multiple threshold tests
def process_file(file, expected_speakers):
    with ThreadPoolExecutor(max_workers=MAX_CONCURRENT_THREADS) as executor:
        for i in range(1, 21):  # testing from 0.1 to 1.0
            threshold = i / 10
            executor.submit(test_threshold, file, expected_speakers, threshold)

threads = []
for file, expected_speakers in files_to_test_with_expected_speakers:
    thread = threading.Thread(target=process_file, args=(file, expected_speakers))
    thread.start()
    threads.append(thread)

for thread in threads:
    thread.join()

print(f"Best threshold is {best_threshold} with an accuracy of {best_accuracy}")
