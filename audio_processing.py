import os
import whisper
import soundfile as sf
from simple_diarizer.diarizer import Diarizer
from tempfile import NamedTemporaryFile
from df.enhance import enhance, init_df, load_audio,save_audio
from pydub import AudioSegment
from pydub.silence import split_on_silence



class AudioEnhancement:
    
    def __init__(self):
        self.model, self.df_state, _ = init_df()
        self.temp_files = []
           
        
    def enhance_audio(self, audio_file):
        audio, sample_rate = load_audio(audio_file)
        print("Enhancing audio...")
        enhanced_audio = enhance(self.model, self.df_state, audio)
        print("Audio enhanced.")
        return enhanced_audio, sample_rate
    
    def enhance_and_save_as_temp_file(self, audio_file):
        enhanced_audio,_=self.enhance_audio(audio_file)
        save_path= "/tmp/"
        df_state = self.df_state
        audio_file_name = audio_file.split('/')[-1].split('.')[0]
        complete_file_name=save_path+audio_file_name+"_enhanced.wav"
        save_audio(complete_file_name, enhanced_audio, df_state.sr())
        print(f"Audio saved as {complete_file_name}")
        return complete_file_name

class Diarization:
    
    def __init__(self, embed_model='xvec', cluster_method='sc'):
        self.temp_files = []
        self.embed_model = embed_model
        self.cluster_method = cluster_method
        self.diar = Diarizer(embed_model=self.embed_model, cluster_method=self.cluster_method)
        self.temp_files = []
        
    
    def load(self, audio_file, threshold=None, num_speakers=None):
        self.audio_file = audio_file
        self.threshold = threshold
        self.segments = []
        self.sample_rate = None
        self.audio = None
        self.file_name = audio_file.split('/')[-1].split('.')[0]
        self.num_speakers = num_speakers
        self.load_audio()
        self.diarize_audio()

    def load_audio(self):
        self.audio, self.sample_rate = sf.read(self.audio_file)
        print(f"Loaded audio with {len(self.audio)} samples at {self.sample_rate} Hz")

    def diarize_audio(self):
        print("Loading diarization model...")
        if self.num_speakers is not None:
            print(f"Diarizing audio with {self.num_speakers} speakers...")
            self.segments = self.diar.diarize(self.audio_file, num_speakers=self.num_speakers)
        else:
            print(f"Diarizing audio with threshold {self.threshold}...")
            self.segments = self.diar.diarize(self.audio_file, threshold=self.threshold)
        for segment in self.segments:
            start_time = segment['start']
            end_time = segment['end']
            label = segment['label']
            start_sample = int(start_time * self.sample_rate)
            end_sample = int(end_time * self.sample_rate)

            print(f"Segment: {label}, Start: {start_time}, End: {end_time}, Start Sample: {start_sample}, End Sample: {end_sample}")
        #Delete the converted audio file
        print("Deleting converted audio file...")
        self.delete_converted_audio()        
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
            self.speaker = segment['speaker']
            start_sample = int(start_time * self.sample_rate)
            end_sample = int(end_time * self.sample_rate)
            segment_audio = self.audio[start_sample:end_sample]

            with NamedTemporaryFile(suffix='.wav', delete=True) as temp_file:
                sf.write(temp_file.name, segment_audio, self.sample_rate)
                # yield the speaker label
                yield {'speaker': self.speaker, 'file_path': temp_file.name}                #yield the temporary file path

    def count_total_speakers(self):
        speaker_ids = set(segment["label"] for segment in self.segments)
        return len(speaker_ids)

    def delete_converted_audio(self):
        #delete if name does not alreay end with _converted.wav
        if not self.audio_file.endswith('_converted.wav'):
            audio_file_path = self.audio_file.split('.')[0]
            os.remove(audio_file_path+'_converted.wav')

class AudioSegmentation:
    
    def __init__(self):
        self.temp_files = []
    
    def load(self, file_path):
        print("Loading audio file...")
        file_format=file_path.split('.')[-1]
        print(f"File format: {file_format}")
        self.file_object = AudioSegment.from_file(file_path, format=file_format)
        print(f"File {file_path} loaded.")
        
    def split_until_less_than_30_seconds(self,file_path):
        print("Splitting audio file until less than 30 seconds...")
        file_format=file_path.split('.')[-1]
        file_object = AudioSegment.from_file(file_path, format=file_format)      
        if file_object.duration_seconds <= 30:
            print(f"yielding {file_path} as it is less than 30 seconds: {file_object.duration_seconds}")
            #Save the file as a temporary file
            with NamedTemporaryFile(suffix='.wav', delete=True) as temp_file:
                file_object.export(temp_file.name, format="wav")
                print(f"Saved temporary file {temp_file.name}")
                yield temp_file.name
        else:
            print(f"Splitting {file_path} of duration {file_object.duration_seconds} into two halves...")
            half = len(file_object) // 2
            left_half = file_object[:half]
            right_half = file_object[half:]
            #Create a temp file for the left half
            with NamedTemporaryFile(suffix='.wav', delete=True) as left_temp_file:
                left_half.export(left_temp_file.name, format="wav")
                for left_segment in self.split_until_less_than_30_seconds(left_temp_file.name):
                    yield left_segment

            #Create a temp file for the right half
            with NamedTemporaryFile(suffix='.wav', delete=True) as right_temp_file:
                right_half.export(right_temp_file.name, format="wav")
                for right_segment in self.split_until_less_than_30_seconds(right_temp_file.name):
                    yield right_segment

            
    def split_on_silence(self, file_path,min_silence_len=1000, silence_thresh=-60, keep_silence=250):
        print("Splitting audio file on silence...")
        file_format=file_path.split('.')[-1]
        file_object = AudioSegment.from_file(file_path, format=file_format)
        segments_silence = split_on_silence(audio_segment=file_object,min_silence_len=min_silence_len, silence_thresh=silence_thresh, keep_silence=keep_silence)
        for segment in segments_silence:
            with NamedTemporaryFile(suffix=f'_segment_{segments_silence.index(segment)}.wav', delete=True) as temp_file:
                file_name = temp_file.name
                segment.export(file_name, format="wav")
                yield file_name
            
class Transcription:
    
    def __init__(self, model_name):
        self.model= whisper.load_model(model_name)
        self.temp_files = []
        
    def transcribe(self, audio_file):
        print(f"Transcribing audio file {audio_file}...")
        transcription=whisper.transcribe(self.model, audio_file)
        print(f"Transcription: {transcription['text']}")
        return transcription