import unittest
from unittest.mock import MagicMock
from service_stt import WhisperSTT
from utility_math import calculate_min_similarity
from utility_log import LogManager 
import logging

lm = LogManager("whisper_logger", logging.INFO)
min_similarity = 0.87


class TestWhisperSTT(unittest.TestCase):
    def setUp(self):
        self.whisper_stt = WhisperSTT('base')


    def test_transcribe_fileTest(self):
        lm.starting_process(self.__class__.__name__, "test_transcribe_successful")
        self.whisper_stt.load_model('auto')
        load_audio= self.whisper_stt.load_audio("src/resources/test_files/mpthreetest.mp3")
        transcription = self.whisper_stt.transcribe(load_audio)
        lm.log('info', f"Transcription: {transcription['text']}")
        expected_test_file = "src/resources/test_files/mpthreetest_expected_output.txt"
        with open(expected_test_file, "r") as file:
            expected_output = file.read()
        lm.log('info', f"Expected output: {expected_output}")
        similarity = calculate_min_similarity(expected_output, transcription['text'])
        lm.log('info', f"similarity: {similarity}")
        self.assertGreater(similarity, min_similarity)
    
    def test_transcribe_monologue(self):
        lm.starting_process(self.__class__.__name__, "test_transcribe_monologue")
        self.whisper_stt.load_model('auto')
        load_audio= self.whisper_stt.load_audio("src/resources/test_files/monologue.ogg")
        transcription = self.whisper_stt.transcribe(load_audio)
        lm.log('info', f"Transcription: {transcription['text']}")
        expected_test_file = "src/resources/test_files/monologue_expected_output.txt"
        with open(expected_test_file, "r") as file:
            expected_output = file.read()
        lm.log('info', f"Expected output: {expected_output}")
        similarity = calculate_min_similarity(expected_output, transcription['text'])
        lm.log('info', f"similarity: {similarity}")
        self.assertGreater(similarity, min_similarity)
    
    def test_transcribe_monologue_wrong_transcription(self):
        lm.starting_process(self.__class__.__name__, "test_transcribe_monologue")
        self.whisper_stt.load_model('auto')
        load_audio= self.whisper_stt.load_audio("src/resources/test_files/monologue.ogg")
        transcription = self.whisper_stt.transcribe(load_audio)
        lm.log('info', f"Transcription: {transcription['text']}")
        expected_test_file = "src/resources/test_files/monologue_unexpected_output.txt"
        with open(expected_test_file, "r") as file:
            expected_output = file.read()
        lm.log('info', f"Expected output: {expected_output}")
        similarity = calculate_min_similarity(expected_output, transcription['text'])
        lm.log('info', f"similarity: {similarity}")
        self.assertLess(similarity, min_similarity)
    
    def test_long_transcription(self):
        lm.starting_process(self.__class__.__name__, "test_long_transcription")
        self.whisper_stt.load_model('auto')
        load_audio= self.whisper_stt.load_audio("src/resources/test_files/fables_01_02_aesop.mp3")
        transcription = self.whisper_stt.transcribe(load_audio)
        lm.log('info', f"Transcription: {transcription['text']}")
        expected_test_file = "src/resources/test_files/fables_01_02_aesop_expected_output.txt"
        with open(expected_test_file, "r") as file:
            expected_output = file.read()
        lm.log('info', f"Expected output: {expected_output}")
        similarity = calculate_min_similarity(expected_output, transcription['text'])
        lm.log('info', f"similarity: {similarity}")
        self.assertGreater(similarity, min_similarity)
        
        
if __name__ == '__main__':
    unittest.main()
  

