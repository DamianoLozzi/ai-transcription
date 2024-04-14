from audio_processing import Diarization,AudioEnhancement, Transcription, AudioSegmentation

diarization = Diarization(embed_model='xvec', cluster_method='sc')
print("Enhancing audio file...")

audio_enhancement = AudioEnhancement()
enhanced_audio = audio_enhancement.enhance_and_save_as_temp_file('/home/ld/Dev/git/ai-assistant/src/resources/test_files/test_long.mp3')

print("Loading audio file...")
diarization.load(enhanced_audio, threshold=0.5)
segments_by_speaker = diarization.segment_audio_by_speaker()

aus=AudioSegmentation()
transcriber=Transcription("tiny")

transcriptions=[]
for temp_file_path in diarization.save_segments_to_files(segments_by_speaker):
    for split_by_silence in aus.split_on_silence(file_path=temp_file_path['file_path']):
        speaker=temp_file_path['speaker']
        for split_by_30_seconds in aus.split_until_less_than_30_seconds(split_by_silence):
            for file_path in aus.split_until_less_than_30_seconds(split_by_silence):
                print("Transcribing file:", file_path)
                transcription = transcriber.transcribe(file_path)
                transcriptions.append({"speaker": speaker, "transcription": transcription['text']})
    


previous_speaker=-1
previous_transcription=''
for transcription in transcriptions:
    speaker=transcription['speaker']
    if previous_speaker!=speaker:
        print("-------------------")
        print("Speaker: ", speaker)
        previous_speaker=speaker
        print("Transcription:")
    if previous_transcription != transcription['transcription']:
        print(transcription['transcription'])
        previous_transcription=transcription['transcription']
        