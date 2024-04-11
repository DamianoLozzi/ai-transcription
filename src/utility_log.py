import logging

class LogManager:
    def __init__(self, name, level=logging.INFO):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        ch = logging.StreamHandler()
        ch.setLevel(level)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)

    def log(self, level, msg):
        if level == 'info':
            self.logger.info(msg)
        elif level == 'error':
            self.logger.error(msg)
        elif level == 'warning':
            self.logger.warning(msg)
        elif level == 'debug':
            self.logger.debug(msg)
        else:
            self.logger.info(msg)
    
    def starting_process(self, class_name, process_name):
        self.log('info', f"Starting process: {class_name}.{process_name}")
    
    def ending_process(self, class_name,process_name, success, message_or_error):
        if success:
            self.log('info', f"Ending process: {class_name}.{process_name}")
        else:
            self.log('error', f"Ending process: {class_name}.{process_name} with error: {message_or_error}")
    
            
class LogMessages:
    START_PROCESS = "Starting process..."
    END_PROCESS = "Ending process..."
    ERROR = "An error occurred"