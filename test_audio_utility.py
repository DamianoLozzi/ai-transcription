from audio_utility import AudioUtility
import os

# Create an instance of AudioUtility
audio_utility = AudioUtility()

# Specify the audio file path and name
audio_path = "src/resources/test_files/"
audio_file = "fables_01_02_aesop.mp3"

# Load and enhance the audio file
enhanced_audio_generator = audio_utility.load_and_enhance_audio(audio_path, audio_file)

# Save the enhanced audio to a temporary file
temp_enhanced_file = next(enhanced_audio_generator)
print("Enhanced audio saved to temporary file:", temp_enhanced_file)

# Split and save segments of the enhanced audio
segment_generator = audio_utility.split_and_save_segments(audio_path, audio_file)

# Iterate over the generated segment file paths
for idx, segment_file in enumerate(segment_generator):
    print(f"Segment {idx + 1} saved to temporary file:", segment_file)

# Clean up temporary files
os.remove(temp_enhanced_file)
for idx in range(4):
    os.remove(f"segment_{idx}.wav") 
