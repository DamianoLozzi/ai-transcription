

import whisper

class WhisperModel:
    _model = None

    def load_model(self):
        model = whisper.load_model('base')
        return model

    def get_instance(self):
        if self._model is None:
            self._model = self.load_model()
        return self._model

    def unload_model(self):
        self._model = None
        return True

    def transcribe_file(self,filename):
        return self.get_instance().transcribe(filename)