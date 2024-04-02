import tempfile
import os
from utility_log import LogManager

lm = LogManager("file_utils_logger")

class FileUtils:
    
    def __init__(self):
        lm.starting_process(self.__class__.__name__, "__init__")
        try:
            lm.ending_process(self.__class__.__name__,
                                "__init__",
                                True,
                                "Object created")
        except Exception as e:
            lm.ending_process(self.__class__.__name__,
                                "__init__",
                                False,
                                f"Object creation failed with error: {str(e)}")
            raise e
    
    def create_temp_file(self, file_content):
        try:
            lm.starting_process(self.__class__.__name__, f"create_temp_file with content: {file_content}")
            temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False)
            temp_file.write(file_content)
            temp_file.close()
            lm.ending_process(self.__class__.__name__, f"create_temp_file: {temp_file.name}", True, f"File created: {temp_file.name}")
            return temp_file
        except Exception as e:
            lm.ending_process(self.__class__.__name__, f"create_temp_file: {temp_file}", False, f"File creation failed with error: {str(e)}")
            raise e
        
    
    def get_temp_file(self, file_name):
        lm.starting_process(self.__class__.__name__, f"get_temp_file: {file_name}")
        try:
            lm.ending_process(self.__class__.__name__, f"get_temp_file: {file_name}", True, f"File retrieved: {file_name}")
            return open(file_name, 'r')
        except FileNotFoundError as e:
            lm.ending_process(self.__class__.__name__,
                                f"get_temp_file: {file_name}",
                                False,
                                f"File not found: {file_name}")
            raise e
    
    
    def delete_temp_file(self, file_name):
        lm.starting_process(self.__class__.__name__, f"delete_temp_file: {file_name}")
        try:
            os.remove(file_name)
            lm.ending_process(self.__class__.__name__, f"delete_temp_file: {file_name}", True, f"File deleted: {file_name}")
        except FileNotFoundError as e:
            lm.ending_process(self.__class__.__name__,
                                f"delete_temp_file: {file_name}",
                                False,
                                f"File not found: {file_name}")
            raise e
        
    def write_on_file(self, file_name, content):
        lm.starting_process(self.__class__.__name__, f"write_on_file: {file_name}")
        try:
            with open(file_name, 'w') as file:
                file.write(content)
            lm.ending_process(self.__class__.__name__, f"write_on_file: {file_name}", True, f"Content written on file: {file_name}")
        except FileNotFoundError as e:
            lm.ending_process(self.__class__.__name__,
                                f"write_on_file: {file_name}",
                                False,
                                f"File not found: {file_name}")
            raise e