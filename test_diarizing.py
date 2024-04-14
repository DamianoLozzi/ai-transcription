from audio_processing import AudioSegmentation

print("Testing AudioSegmentation class...")
audio_segmentation = AudioSegmentation(embed_model='xvec', cluster_method='sc')
print("Loading audio file...")
audio_segmentation.load('/home/ld/Dev/git/ai-assistant/src/resources/test_files/fables_01_02_aesop.mp3', threshold=2)
segments_by_speaker = audio_segmentation.segment_audio_by_speaker()
for temp_file_path in audio_segmentation.save_segments_to_files(segments_by_speaker):
    print("Speaker: ", temp_file_path['speaker'])
    print("Temporary file path:", temp_file_path['file_path'])
total_speakers = audio_segmentation.count_total_speakers()
print("Total number of speakers:", total_speakers)