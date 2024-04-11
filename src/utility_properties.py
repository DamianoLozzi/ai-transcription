import os

from jproperties import Properties
from utility_log import LogManager


lm= LogManager("whisper_logger")
configs= Properties()


class PropertiesManager:
    def __init__(self, filepath):
        # Get the directory of this script
        script_dir = os.path.dirname(os.path.abspath(__file__))

        # Construct the absolute path to the properties file
        abs_filepath = os.path.join(script_dir, filepath)

        lm.starting_process(self.__class__.__name__, f"__init__: {abs_filepath}")
        try:
            with open(abs_filepath, 'rb') as config_file:
                configs.load(config_file)
            lm.ending_process(self.__class__.__name__,
                                f"__init__: {abs_filepath}",
                                True,
                                f"Properties loaded from file: {abs_filepath}")
        except Exception as e:
            lm.ending_process(self.__class__.__name__,
                                f"__init__: {abs_filepath}",
                                False,
                                f"Properties loading failed with error: {str(e)}")
            raise e
            
        

    def get_property(self, key):
        lm.starting_process(self.__class__.__name__, f"get_property: {key}")
        value_meta = configs.get(key)
        if value_meta is None:
            lm.ending_process(self.__class__.__name__, f"get_property: {key}", False, f"Property not found: {key}")
            raise KeyError(f"Property not found: {key}")
        else:
            value= value_meta[0]
            lm.log('info', f"Property found: Key: {key}, Value: {value}")
        lm.ending_process(self.__class__.__name__, f"get_property: {key}", True, f"Value: {value}")
        return value

