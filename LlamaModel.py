

from llama_cpp import Llama

class LlamaModel:
    _model = None

    def __init__(self):
        self._model = Llama(model_path="./models/llama-2-7b-chat.Q2_K.gguf")
        

    def get_instance(self):
        if self._model is None:
            self._model = self.load_model()
        return self._model
    
    def unload_model(self):
        self._model = None
        return True

    def generate(self, instruction):
        return self._model(instruction)
    
