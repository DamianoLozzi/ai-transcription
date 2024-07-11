import sys
import os
from langchain_community.llms import LlamaCpp

# enable verbose to debug the LLM's operation
verbose = False

llm = LlamaCpp(
    #get the path of the script from os
    model_path="/home/ld/Dev/git/ai-assistant/models/ggml-model-q4_0.gguf",
    # max tokens the model can account for when processing a response
    # make it large enough for the question and answer
    n_ctx=4096,
    # number of layers to offload to the GPU 
    # GPU is not strictly required but it does help
    n_gpu_layers=32,
    # number of tokens in the prompt that are fed into the model at a time
    n_batch=1024,
    # use half precision for key/value cache; set to True per langchain doc
    f16_kv=True,
    verbose=verbose,
)

question = "generate a title for this text: This is a Librivox recording. All Librivox recordings are in the public domain. For more information or to volunteer, please visit Librivox.org. ASOP'S FABELS, THE GOOSE THAT LAID THE GOLDEN EGGS. A man and his wife had the good fortune to possess a goose, which laid a golden egg every day. Lucky though they were, they soon began to think that they were not getting rich fast enough, and, imagining the bird must be made of gold inside, they decided to kill it in order to secure the whole store of precious metal at once. But, when they cut it open, they found it was just like any other goose. Thus, they neither got rich all at once as they had hoped, nor enjoyed any longer the daily addition to their wealth. Much once more, and loses all.  end of the goose that laid the golden eggs."
output = llm.invoke(
    question,
    max_tokens=1024,
    temperature=0.2,
    # nucleus sampling (mass probability index)
    # controls the cumulative probability of the generated tokens
    # the higher top_p the more diversity in the output
    top_p=0.1
)

print(f"\n{output}")

'''
while True:
    question = input("Ask me a question: ")
    if question == "stop":
        sys.exit(1)
    output = llm.invoke(
        question,
        max_tokens=4096,
        temperature=0.2,
        # nucleus sampling (mass probability index)
        # controls the cumulative probability of the generated tokens
        # the higher top_p the more diversity in the output
        top_p=0.1
    )
    print(f"\n{output}") 
'''