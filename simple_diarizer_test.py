import soundfile as sf
from simple_diarizer.diarizer import Diarizer



AUDIO_FILE = 'src/resources/test_files/fables_01_02_aesop.mp3'
THRESHOLD = 0.5
FILE_NAME = AUDIO_FILE.split('/')[-1].split('.')[0]
print("loading model")
diar = Diarizer(
    embed_model='xvec',  # 'xvec' and 'ecapa' supported
    cluster_method='sc'  # 'ahc' and 'sc' supported
)
segments = diar.diarize(AUDIO_FILE, num_speakers=None, threshold=THRESHOLD)
#segments = diar.diarize(AUDIO_FILE, num_speakers=3)


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

segment_counter = 0
cycle_counter = 0

segments_by_speaker = []

while segment_counter < len(segments):
    cycle_counter += 1
    segment = segments[segment_counter]
    start_time = segment['start']
    current_speaker = segment['label']
    end_time = start_time

    # find the segment in which the speaker changes
    while segment_counter < len(segments) and segments[segment_counter]['label'] == current_speaker:
        end_time = segments[segment_counter]['end']
        segment_counter += 1
    
    segments_by_speaker.append({ 'speaker': current_speaker, 'start': start_time, 'end': end_time })

print(f"Segments by speaker: {segments_by_speaker}")

# Save the segments to separate files
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
    segment_audio = audio[start_sample:end_sample]
    sf.write(f"{FILE_NAME}_{curr_segment}_{speaker}.wav", segment_audio, sample_rate)
    
# Extract speaker IDs
speaker_ids = set(segment["label"] for segment in segments)

# Count the total number of speakers
total_speakers = len(speaker_ids)

print("Total number of speakers:", total_speakers)
