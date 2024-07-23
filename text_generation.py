import psutil
import torch
import re
from typing import Literal
import languagemodels as lm
import custom_logger as log
from datetime import datetime


def bytes_to_gb(bytes) -> float:
    try:
        return bytes / 1024**3
    except Exception as e:
        log.error(f"Error converting bytes to GB: {e}")

def select_model_based_on_resources() -> float:
    try:
        log.debug("Selecting model based on available resources")
        cuda_available : bool = torch.cuda.is_available()

        if cuda_available:
            log.debug("CUDA is available")
            video_ram_gb : float = bytes_to_gb(torch.cuda.get_device_properties(0).total_memory)
            max_ram : float = select_model_based_on_ram(video_ram_gb)
        else:
            log.debug("CUDA is not available")
            total_ram__gb : float = bytes_to_gb(psutil.virtual_memory().total)
            log.debug(f"Total RAM: {total_ram__gb:.2f} GB")
            available_ram_gb : float = bytes_to_gb(psutil.virtual_memory().available)
            log.debug(f"Available RAM: {available_ram_gb:.2f} GB")
            cores_num : int = psutil.cpu_count(logical=True)
            log.debug(f"Number of cores: {cores_num}")
            max_ram : float = select_model_based_on_cpu(available_ram_gb, cores_num)
        
        return max_ram
    except Exception as e:
        log.error(f"Error selecting model: {e}")


def select_model_based_on_ram(ram_gb) -> float:
    try:
        log.debug(f"Selecting model based on RAM: {ram_gb} GB")
        selected_ram_value : float = 0.5
        
        if ram_gb >= 8:
            selected_ram_value = 8
        elif ram_gb >= 4:
            selected_ram_value = 4
        elif ram_gb >= 2:
            selected_ram_value = 2
        elif ram_gb >= 1:
            selected_ram_value = 1
    
        log.debug(f"Selected RAM value: {selected_ram_value}")
        return selected_ram_value
    except Exception as e:
        log.error(f"Error selecting model based on RAM: {e}")
    

def select_model_based_on_cpu(ram_gb, cores) -> float:
    try:
        if cores < 4:
            log.debug("CPU has less than 4 cores, selecting 0.5 GB RAM")
            return 0.5
        else:
            log.debug("CPU has 4 or more cores, based on {ram_gb} GB RAM")
        return select_model_based_on_ram(ram_gb)
    except Exception as e:
        log.error(f"Error selecting model based on CPU: {e}")
    

max_ram = select_model_based_on_resources()


def generate_name(text, type: Literal['filename','title']) -> str:
    try:
        log.debug(f"Generating file name for text: {text}")
        name = lm.do(f"generate a short title for this text: {text}")
        log.debug(f"Generated file name: {name}")
        name= re.sub(r"[^ a-zA-Z0-9]+",'',name).strip()
        if type == 'filename':
            name=name.replace(" ", "_").lower() + "_" + str(datetime.now().strftime("%Y%m%d%H%M%S"))
            
        return name
    except Exception as e:
        log.error(f"Error generating file name: {e}")
        
def generate_summary(text) -> str:
    try:
        log.debug(f"Generating summary for text: {text}")
        summary = lm.do(f"generate a summary for this text: {text}")
        log.debug(f"Generated summary: {summary}")
        return summary
    except Exception as e:
        log.error(f"Error generating summary: {e}")