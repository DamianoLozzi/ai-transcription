import transformers
import torch

model_id = "TinyLlama/TinyLlama_v1.1"


pipeline = transformers.pipeline(
    "text-generation",
    model=model_id,
    model_kwargs={"torch_dtype": torch.bfloat16},
    device_map= 'cuda:0' if torch.cuda.is_available() else 'cpu')

print(pipeline.model.devices)
pipeline("Hey how are you doing today?")