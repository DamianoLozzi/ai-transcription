from pydub import AudioSegment
from pydub.silence import split_on_silence
from df.enhance import enhance, init_df, load_audio, save_audio
import threading
import tempfile
import os

class AudioUtility:
    def __init__(self):
        self.model, self.df_state, _ = init_df()
        print("Model loaded")

    def split_audio(self, file_object):
        def split_until_less_than_30_seconds(file_obj):
            if file_obj.duration_seconds <= 30:
                yield file_obj
            else:
                half = len(file_obj) // 2
                left_half = file_obj[:half]
                right_half = file_obj[half:]

                left_segments = split_until_less_than_30_seconds(left_half)
                right_segments = split_until_less_than_30_seconds(right_half)

                yield from left_segments
                yield from right_segments

        yield from split_until_less_than_30_seconds(file_object)

    def enhance_audio(self, audio_file):
        enhanced_audio = enhance(self.model, self.df_state, audio_file)
        yield enhanced_audio

    def load_and_enhance_audio(self, audio_path, audio_file):
        audio_file_path = audio_path + audio_file
        audio_file, _ = load_audio(audio_file_path)
        yield from self.enhance_audio(audio_file)

    def split_and_save_segments(self, audio_path, audio_file):
        audio_file_path = audio_path + audio_file
        file_object = AudioSegment.from_file(audio_file_path, format="mp3")
        segments_silence = split_on_silence(file_object, min_silence_len=1000, silence_thresh=-60, keep_silence=250)

        for segment in segments_silence:
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
                temp_filename = temp_file.name
                segment.export(temp_filename, format="wav")
                yield temp_filename
                print(f"Segment not silent duration: {segment.duration_seconds}")
