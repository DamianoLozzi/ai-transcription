from diarizing import AudioSegmentation


audio_segmentation = AudioSegmentation('src/resources/test_files/LE_listening_A2_Changing_a_meeting_time.mp3')
segments_by_speaker = audio_segmentation.segment_audio_by_speaker()
for temp_file_path in audio_segmentation.save_segments_to_files(segments_by_speaker):
    print("Temporary file path:", temp_file_path)
total_speakers = audio_segmentation.count_total_speakers()
print("Total number of speakers:", total_speakers)