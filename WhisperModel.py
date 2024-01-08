

from whisper import load_model, transcribe

class WhisperModel:
    _model = None

    def __init__(self):
        self._model = self.load()
    
    def get_instance(self):
        if self._model is None:
            self._model = self.load()
        return self

    def load(self):
        model = load_model('base')
        return model

    def unload_model(self):
        self._model = None
        return True

    def transcribe_file(self, filename):
        return self._model.transcribe(filename)