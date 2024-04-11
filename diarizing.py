import soundfile as sf
from simple_diarizer.diarizer import Diarizer
from tempfile import NamedTemporaryFile

class AudioSegmentation:
    def __init__(self, audio_file, embed_model='xvec', cluster_method='sc', threshold=0.01):
        self.audio_file = audio_file
        self.embed_model = embed_model
        self.cluster_method = cluster_method
        self.threshold = threshold
        self.segments = []
        self.sample_rate = None
        self.audio = None
        self.file_name = audio_file.split('/')[-1].split('.')[0]
        self.load_audio()
        self.diarize_audio()

    def load_audio(self):
        self.audio, self.sample_rate = sf.read(self.audio_file)
        print(f"Loaded audio with {len(self.audio)} samples at {self.sample_rate} Hz")

    def diarize_audio(self):
        print("Loading diarization model...")
        diar = Diarizer(embed_model=self.embed_model, cluster_method=self.cluster_method)
        self.segments = diar.diarize(self.audio_file, threshold=self.threshold)
        print("Diarization complete.")

    def segment_audio_by_speaker(self):
        segments_by_speaker = []
        segment_counter = 0

        while segment_counter < len(self.segments):
            segment = self.segments[segment_counter]
            start_time = segment['start']
            current_speaker = segment['label']
            end_time = start_time

            while segment_counter < len(self.segments) and self.segments[segment_counter]['label'] == current_speaker:
                end_time = self.segments[segment_counter]['end']
                segment_counter += 1

            segments_by_speaker.append({'speaker': current_speaker, 'start': start_time, 'end': end_time})

        return segments_by_speaker

    def save_segments_to_files(self, segments_by_speaker):
        for idx, segment in enumerate(segments_by_speaker):
            start_time = segment['start']
            end_time = segment['end']
            speaker = segment['speaker']
            start_sample = int(start_time * self.sample_rate)
            end_sample = int(end_time * self.sample_rate)
            segment_audio = self.audio[start_sample:end_sample]

            with NamedTemporaryFile(suffix='.wav', delete=False) as temp_file:
                sf.write(temp_file.name, segment_audio, self.sample_rate)
                yield temp_file.name

    def count_total_speakers(self):
        speaker_ids = set(segment["label"] for segment in self.segments)
        return len(speaker_ids)


