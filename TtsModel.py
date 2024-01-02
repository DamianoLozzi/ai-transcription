

from transformers import AutoProcessor, AutoModel


class TtsModel:
    _processor = None
    _model = None
    _sample_rate = None
    
    def load_model(self):
        processor = AutoProcessor.from_pretrained("suno/bark-small")
        model = AutoModel.from_pretrained("suno/bark-small")
        sample_rate = model.generation_config.sample_rate
        return processor, model, sample_rate
    
    def get_instance(self):
        if self._processor is None:
            self._processor, self._model, self._sample_rate = self.load_model()
        return self._processor, self._model, self._sample_rate
    
    def unload_model(self):
        self._processor = None
        self._model = None
        self._sample_rate = None
        return True
    