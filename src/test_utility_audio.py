import unittest
from utility_audio import audio_length,split_in_chunks,process_long_audio

class TestUtilityAudio(unittest.TestCase):
   
    def test_split_in_chunks(self):
        audio_file="src/resources/test_files/monologue.ogg"
        chunks = split_in_chunks(audio_file)
        self.assertEquals(len(chunks), 13)

  
if __name__ == "__main__":
    unittest.main()