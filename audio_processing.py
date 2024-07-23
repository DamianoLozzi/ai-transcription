import os
import whisper
import soundfile as sf
from simple_diarizer.diarizer import Diarizer
from tempfile import NamedTemporaryFile
from df.enhance import enhance, init_df, load_audio,save_audio
from pydub import AudioSegment
from pydub.silence import split_on_silence
import custom_logger as log 
import torch
import psutil

class AudioEnhancement:
    
    def __init__(self):
        self.model, self.df_state, _ = init_df()
        self.temp_files = []
           
        
    def enhance_audio(self, audio_file):
        try:
            audio, sample_rate = load_audio(audio_file)
            log.info("Enhancing audio...")
            enhanced_audio = enhance(self.model, self.df_state, audio)
            log.info("Audio enhanced.")
            return enhanced_audio, sample_rate
        except Exception as e:
            log.error(f"Error enhancing audio: {e}")
            return None, None
    
    def enhance_and_save_as_temp_file(self, audio_file):
        enhanced_audio, sample_rate = self.enhance_audio(audio_file)
        if enhanced_audio is not None:
            try:
                with NamedTemporaryFile(delete=False, suffix=".wav", dir="/tmp") as temp_file:
                    save_audio(temp_file.name, enhanced_audio, sample_rate)
                    log.info(f"Audio saved as {temp_file.name}")
                    self.temp_files.append(temp_file.name)
                    return temp_file.name
            except Exception as e:
                log.error(f"Error saving enhanced audio: {e}")
                return None
        else:
            return None

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
        try:
            self.audio, self.sample_rate = sf.read(self.audio_file)
            log.info(f"Loaded audio with {len(self.audio)} samples at {self.sample_rate} Hz")
        except Exception as e:
            log.error(f"Error loading audio: {e}")
            return None, None

    def diarize_audio(self):
        try:
            log.info("Loading diarization model...")
            if self.num_speakers is not None:
                log.info(f"Diarizing audio with {self.num_speakers} speakers...")
                self.segments = self.diar.diarize(self.audio_file, num_speakers=self.num_speakers)
            else:
                log.info(f"Diarizing audio with threshold {self.threshold}...")
                self.segments = self.diar.diarize(self.audio_file, threshold=self.threshold)
            for segment in self.segments:
                start_time = segment['start']
                end_time = segment['end']
                label = segment['label']
                start_sample = int(start_time * self.sample_rate)
                end_sample = int(end_time * self.sample_rate)

                log.info(f"Segment: {label}, Start: {start_time}, End: {end_time}, Start Sample: {start_sample}, End Sample: {end_sample}")
            #Delete the converted audio file
            file_name=self.audio_file.split('/')[-1].split('.')[0]+"_converted.wav"
            log.info("Deleting converted audio file {}".format(file_name))
            os.remove("/tmp/"+file_name)
            log.info("Diarization complete.")
        except Exception as e:
            log.error(f"Error diarizing audio: {e}")
            return None


    def segment_audio_by_speaker(self):
        try:
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
        except Exception as e:
            log.error(f"Error segmenting audio by speaker: {e}")
            return None

    def save_segments_to_files(self, segments_by_speaker):
        try:
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
                    yield {'speaker': self.speaker, 'file_path': temp_file.name}   
        except Exception as e:
            log.error(f"Error saving segments to files: {e}")
            return None

        def count_total_speakers(self):
            try:
                speaker_ids = set(segment["label"] for segment in self.segments)
                return len(speaker_ids)
            except Exception as e:
                log.error(f"Error counting total speakers: {e}")
                return None

        def delete_converted_audio(self):
            try:
                if not self.audio_file.endswith('_converted.wav'):
                    audio_file_path = self.audio_file.split('.')[0]
                    os.remove(audio_file_path+'_converted.wav')
            except Exception as e:
                log.error(f"Error deleting converted audio: {e}")
                return None 
        

class AudioSegmentation:
    
    def __init__(self):
        self.temp_files = []
    
    def load(self, file_path):
        log.info("Loading audio file...")
        file_format=file_path.split('.')[-1]
        log.info(f"File format: {file_format}")
        self.file_object = AudioSegment.from_file(file_path, format=file_format)
        log.info(f"File {file_path} loaded.")
        
    def split_until_less_than_30_seconds(self,file_path):
        try:
            log.info("Splitting audio file until less than 30 seconds...")
            file_format=file_path.split('.')[-1]
            file_object = AudioSegment.from_file(file_path, format=file_format)      
            if file_object.duration_seconds <= 30:
                log.info(f"yielding {file_path} as it is less than 30 seconds: {file_object.duration_seconds}")
                #Save the file as a temporary file
                with NamedTemporaryFile(suffix='.wav', delete=True) as temp_file:
                    file_object.export(temp_file.name, format="wav")
                    log.info(f"Saved temporary file {temp_file.name}")
                    yield temp_file.name
            else:
                log.info(f"Splitting {file_path} of duration {file_object.duration_seconds} into two halves...")
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
        except Exception as e:
            log.error(f"Error splitting audio file: {e}")
            return None
        

            
    def split_on_silence(self, file_path,min_silence_len=1000, silence_thresh=-60, keep_silence=250):
        try:
            file_format=file_path.split('.')[-1]
            log.info("Splitting audio file {file_path}  with format {file_format} on silence...")
            file_object = AudioSegment.from_file(file_path, format=file_format)
            segments_silence = split_on_silence(audio_segment=file_object,min_silence_len=min_silence_len, silence_thresh=silence_thresh, keep_silence=keep_silence)
            for segment in segments_silence:
                with NamedTemporaryFile(suffix=f'_segment_{segments_silence.index(segment)}.wav', delete=True) as temp_file:
                    file_name = temp_file.name
                    segment.export(file_name, format="wav")
                    yield file_name
        except Exception as e:
            log.error(f"Error splitting audio file on silence: {e}")
            return None
            
class Transcription:
    
    def __init__(self, model_name):
        if model_name == "auto":
            log.info("Evaluating model based on resources...")
            model_name= self.select_model_based_on_resources()
            log.info(f"Selected model: {model_name}")
        log.debug(f"Loading model {model_name}...")
        self.model= whisper.load_model(model_name)
        self.temp_files = []
        
    def bytes_to_gb(self,bytes) -> float:
        try:
            return bytes / 1024**3
        except Exception as e:
            log.error(f"Error converting bytes to GB: {e}")
        
    def select_model_based_on_resources(self):
        try:
            cuda_available = torch.cuda.is_available()
            if cuda_available:
                log.debug("CUDA is available")
                video_ram_gb = self.bytes_to_gb(torch.cuda.get_device_properties(0).total_memory)
                max_ram = self.select_model_based_on_ram(video_ram_gb)
            else:
                log.debug("CUDA is not available")
                total_ram_gb = self.bytes_to_gb(psutil.virtual_memory().total)
                log.debug(f"Total RAM: {total_ram_gb:.2f} GB")
                available_ram_gb = self.bytes_to_gb(psutil.virtual_memory().available)
                log.debug(f"Available RAM: {available_ram_gb:.2f} GB")
                cores_num = psutil.cpu_count(logical=True)
                log.debug(f"Number of cores: {cores_num}")
                max_ram = self.select_model_based_on_cpu(available_ram_gb, cores_num)
            return max_ram
        except Exception as e:
            log.error(f"Error selecting model: {e}")
            return None
        
    def select_model_based_on_ram(self,ram_gb):
        try:
            selected_model= "tiny"
            if ram_gb >= 16:
                selected_model = "large"
            elif ram_gb >= 8:
                selected_model = "medium"
            elif ram_gb >= 4:
                selected_model = "small"
            log.debug(f"Selected RAM value: {selected_model}")
            return selected_model
        except Exception as e:
            log.error(f"Error selecting model based on RAM: {e}")
            return None
        
    def select_model_based_on_cpu(self,ram_gb, cores):
        try:
            log.debug(f"Evaluating CPU resources: {ram_gb} GB RAM, {cores} cores")
            if cores < 4:
                log.debug("CPU has less than 4 cores, selecting 0.5 GB RAM")
                return "tiny"
            else:
                log.debug("CPU has 4 or more cores, based on {ram_gb} GB RAM")
            return self.select_model_based_on_ram(ram_gb)
        except Exception as e:
            log.error(f"Error selecting model based on CPU: {e}")
            return None
    
        
    def transcribe(self, audio_file):
        try:
            log.info(f"Transcribing audio file {audio_file}...")
            transcription=whisper.transcribe(self.model, audio_file)
            log.debug(f"Transcription: {transcription['text']}")
            return transcription
        except Exception as e:
            log.error(f"Error transcribing audio: {e}")
            return None