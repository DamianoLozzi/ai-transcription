

from transformers import AutoProcessor, AutoModel
from bark import SAMPLE_RATE, generate_audio, preload_models
from scipy.io.wavfile import write as write_wav

class TtsModel:

    def __init__(self):
        preload_models()

    def speak(self,text):
        return generate_audio(text)

    @property
    def SAMPLE_RATE(self):
        return SAMPLE_RATE
        
