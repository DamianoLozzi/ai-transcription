import logging
import unittest
from unittest.mock import patch
from utility_log import LogManager

class TestLogManager(unittest.TestCase):
    def setUp(self):
        self.log_manager = LogManager("test_logger", level=logging.DEBUG)

    def tearDown(self):
        pass

    def test_log_info(self):
        with patch('logging.Logger.info') as mock_info:
            self.log_manager.log('info', 'Test message')
            mock_info.assert_called_with('Test message')

    def test_log_error(self):
        with patch('logging.Logger.error') as mock_error:
            self.log_manager.log('error', 'Test error message')
            mock_error.assert_called_with('Test error message')

    def test_log_warning(self):
        with patch('logging.Logger.warning') as mock_warning:
            self.log_manager.log('warning', 'Test warning message')
            mock_warning.assert_called_with('Test warning message')

    def test_log_debug(self):
        with patch('logging.Logger.debug') as mock_debug:
            self.log_manager.log('debug', 'Test debug message')
            mock_debug.assert_called_with('Test debug message')

    def test_log_default(self):
        with patch('logging.Logger.info') as mock_info:
            self.log_manager.log('unknown', 'Test default message')
            mock_info.assert_called_with('Test default message')

    def test_starting_process(self):
        with patch('logging.Logger.info') as mock_info:
            self.log_manager.starting_process('TestClass', 'test_process')
            mock_info.assert_called_with('Starting process: TestClass.test_process')

    def test_ending_process_success(self):
        with patch('logging.Logger.info') as mock_info:
            self.log_manager.ending_process('TestClass', 'test_process', True, '')
            mock_info.assert_called_with('Ending process: TestClass.test_process')

    def test_ending_process_failure(self):
        with patch('logging.Logger.error') as mock_error:
            self.log_manager.ending_process('TestClass', 'test_process', False, 'Error message')
            mock_error.assert_called_with('Ending process: TestClass.test_process with error: Error message')

if __name__ == '__main__':
    unittest.main()