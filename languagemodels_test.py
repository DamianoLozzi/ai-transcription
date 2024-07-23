import languagemodels as lm
import psutil

def bytes_to_gb(bytes) -> float:
    return bytes / 1024**3


total_ram_gb = bytes_to_gb(psutil.virtual_memory().total)
available_ram_gb = bytes_to_gb(psutil.virtual_memory().available)
cores_num = psutil.cpu_count(logical=True)

print(f"Total RAM: {total_ram_gb:.2f} GB")
print(f"Available RAM: {available_ram_gb:.2f} GB")
print(f"Number of cores: {cores_num}")

lm.config["device"] = "auto"
#lm.config["max_ram"] = available_ram_gb / 2
lm.config["max_ram"] = 8

first = lm.do("generate a short title for this text: This is a Librivox recording. All Librivox recordings are in the public domain. For more information or to volunteer, please visit Librivox.org. ASOP'S FABELS, THE GOOSE THAT LAID THE GOLDEN EGGS. A man and his wife had the good fortune to possess a goose, which laid a golden egg every day. Lucky though they were, they soon began to think that they were not getting rich fast enough, and, imagining the bird must be made of gold inside, they decided to kill it in order to secure the whole store of precious metal at once. But, when they cut it open, they found it was just like any other goose. Thus, they neither got rich all at once as they had hoped, nor enjoyed any longer the daily addition to their wealth. Much once more, and loses all.  end of the goose that laid the golden eggs.")

print(first.replace(" ", "_").lower())

print(lm.do("generate a short title for this text:Ok, we are trying this for a second time to test the ability to upload an mp3 file. Hopefully this will work."))