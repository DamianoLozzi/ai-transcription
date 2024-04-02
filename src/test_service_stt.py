import unittest
from unittest.mock import MagicMock
from service_stt import WhisperSTT
from utility_math import calculate_cosine_similarity
from utility_log import LogManager 
import logging

lm = LogManager("whisper_logger", logging.INFO)

class TestWhisperSTT(unittest.TestCase):
    def setUp(self):
        self.whisper_stt = WhisperSTT('base')


    def test_transcribe_successful(self):
        lm.starting_process(self.__class__.__name__, "test_transcribe_successful")
        self.whisper_stt.load_model('auto')
        load_audio= self.whisper_stt.load_audio("src/resources/test_files/mpthreetest.mp3")
        transcription = self.whisper_stt.transcribe(load_audio)
        lm.log('info', f"Transcription: {transcription['text']}")
        expected_test_file = "src/resources/test_files/mpthreetest_expected_output.txt"
        with open(expected_test_file, "r") as file:
            expected_output = file.read()
        lm.log('info', f"Expected output: {expected_output}")
        cosine_similarity = calculate_cosine_similarity(expected_output, transcription['text'])
        lm.log('info', f"cosine_similarity: {cosine_similarity}")
        self.assertGreater(cosine_similarity, 0.9)
        
 
        
    

if __name__ == '__main__':
    unittest.main()
  

