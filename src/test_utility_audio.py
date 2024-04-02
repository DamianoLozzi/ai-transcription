import unittest
from utility_audio import audio_length,split_in_chunks,process_long_audio

class TestUtilityAudio(unittest.TestCase):

    def test_audio_length(self):
        audio_file="src/resources/test_files/monologue.ogg"
        al = audio_length(audio_file)
        # Check if the audio length is between 124 and 125 seconds
        self.assertGreaterEqual(al, 124)
        self.assertLessEqual(al, 125)
        
    def test_split_in_chunks(self):
        audio_file="src/resources/test_files/monologue.ogg"
        chunk_length=10
        chunks = split_in_chunks(audio_file, chunk_length)
        self.assertEquals(len(chunks), 13)
        
    def test_process_long_audio(self):
        audio_file="src/resources/test_files/monologue.ogg"
        chunk_length_ms=10000
        files = process_long_audio(audio_file, chunk_length_ms)
        self.assertEquals(len(files), 13)
  
if __name__ == "__main__":
    unittest.main()