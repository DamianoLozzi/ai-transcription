import unittest
from unittest.mock import patch
from utility_files import FileUtils
import os

class TestFileUtils(unittest.TestCase):

    def test_create_temp_file(self):
        file_content = "This is a test file."
        file_utils = FileUtils()
        temp_file = file_utils.create_temp_file(file_content)
        self.assertTrue(os.path.exists(temp_file.name))
        with open(temp_file.name, 'r') as f:
            self.assertEqual(f.read(), file_content)
        file_utils.delete_temp_file(temp_file.name)
        self.assertFalse(os.path.exists(temp_file.name))

    def test_get_temp_file(self):
        file_content = "This is a test file."
        file_utils = FileUtils()
        temp_file = file_utils.create_temp_file(file_content)
        retrieved_file = file_utils.get_temp_file(temp_file.name)
        self.assertEqual(retrieved_file.read(), file_content)
        retrieved_file.close()
        file_utils.delete_temp_file(temp_file.name)

    def test_delete_temp_file(self):
        file_content = "This is a test file."
        file_utils = FileUtils()
        temp_file = file_utils.create_temp_file(file_content)
        file_utils.delete_temp_file(temp_file.name)
        self.assertFalse(os.path.exists(temp_file.name))

    
if __name__ == '__main__':
    unittest.main()