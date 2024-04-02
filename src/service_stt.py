import whisper
import logging
from utility_log import LogManager
from utility_properties import PropertiesManager
import psutil

# Configure logging
lm = LogManager("whisper_logger", logging.INFO)

class WhisperSTT:
    def __init__(self, model_name):
        pm = PropertiesManager('resources/application.properties')
        self.model = self.load_model(pm.get_property('whisper.model'))
        
    def select_model(self, model_name):
        lm.starting_process(self.__class__.__name__, "load_model")
        lm.log('info', f"Loading model: {model_name}")
        try:
            if model_name not in ['tiny', 'base', 'small', 'medium', 'large', 'auto']:
                lm.ending_process(self.__class__.__name__, "load_model", False, f"Invalid model name: {model_name}")
                raise ValueError(f"Invalid model name: {model_name}")
            elif model_name == 'auto':
                return self.auto_select(self.get_system_ram())
            else:
                lm.log('info', f"Loading model: {model_name}")
                return model_name
        except Exception as e:
            lm.ending_process(self.__class__.__name__,
                                 "load_model",
                                 False,
                                 f"Model loading failed with error: {str(e)}")
            raise e
        
    def auto_select(self, system_ram):
        lm.starting_process(self.__class__.__name__, "auto_select")
        try:
            lm.log('info', f"System RAM: {system_ram}")
            #if system ram is less than 4GB, return the tiny model
            if system_ram < 4e9:
                lm.ending_process(self.__class__.__name__, "auto_select", True, "Tiny model selected")
                return 'tiny'
            #if system ram is less than 8GB, return the base model
            elif system_ram < 8e9:
                lm.ending_process(self.__class__.__name__, "auto_select", True, "Base model selected")
                return 'base'
            #if system ram is less than 16GB, return the small model
            elif system_ram < 16e9:
                lm.ending_process(self.__class__.__name__, "auto_select", True, "Small model selected")
                return 'small'
            #if system ram is less than 32GB, return the medium model
            elif system_ram < 32e9:
                lm.ending_process(self.__class__.__name__, "auto_select", True, "Medium model selected")
                return 'medium'
            #else return the large model
            else:
                lm.ending_process(self.__class__.__name__, "auto_select", True, "Large model selected")
                return 'large'
        except Exception as e:
            lm.ending_process(self.__class__.__name__,
                                 "auto_select",
                                 False,
                                 f"Model selection failed with error: {str(e)}")
            raise e
        
    def load_model(self, model_name):
        lm.starting_process(self.__class__.__name__, "load_model")
        lm.log('info', f"Loading model: {model_name}")
        try:
            self.model = whisper.load_model(self.select_model(model_name))
            lm.ending_process(self.__class__.__name__, "load_model", True, f"Model {model_name} loaded successfully")
        except Exception as e:
            lm.ending_process(self.__class__.__name__,
                                 "load_model",
                                 False,
                                 f"Model loading failed with error: {str(e)}")
            raise e
        
    def transcribe(self, audio):
        lm.starting_process(self.__class__.__name__, "transcribe")
        lm.log('info', "Transcribing audio...")
        try:
            transcription= whisper.transcribe(self.model, audio)
            lm.ending_process(self.__class__.__name__, "transcribe", True, "Transcription successful")
            return transcription
        except Exception as e:
            lm.ending_process(self.__class__.__name__,
                                 "transcribe",
                                 False,
                                 f"Transcription failed with error: {str(e)}")
            raise e
        
    def load_audio(self, audio_file):
        lm.starting_process(self.__class__.__name__, "load_audio")
        lm.log('info', f"Loading audio file: {audio_file}")
        try:
            audio = whisper.load_audio(audio_file)
            lm.ending_process(self.__class__.__name__, "load_audio", True, f"Audio file {audio_file} loaded successfully")
            return audio
        except Exception as e:
            lm.ending_process(self.__class__.__name__,
                                 "load_audio",
                                 False,
                                 f"Audio loading for {audio_file} failed with error: {str(e)}")
            raise e 
        
    def get_system_ram(self):
        return psutil.virtual_memory().total         
        
        
        
        
