import unittest
from unittest.mock import patch, mock_open
from utility_properties import PropertiesManager

class TestPropertiesManager(unittest.TestCase):
    def test_init_success(self):
        filepath = "resources/test_files/test.properties"
        properties_manager = PropertiesManager(filepath)
        self.assertEqual(properties_manager.get_property("whisper_test1"), "auto")
        
    def test_init_failure(self):
        filepath = "resources/test_files/invalid.properties"
        with self.assertRaises(Exception):
            PropertiesManager(filepath)
            
    def test_get_property_success(self):
        filepath = "resources/test_files/test.properties"
        properties_manager = PropertiesManager(filepath)
        self.assertEqual(properties_manager.get_property("whisper_test1"), "auto")
        self.assertEqual(properties_manager.get_property("whisper_test2"), "tiny")
        self.assertEqual(properties_manager.get_property("whisper_test3"), "small")
        self.assertEqual(properties_manager.get_property("whisper_test4"), "medium")
        self.assertEqual(properties_manager.get_property("whisper_test5"), "large")
        
    def test_get_nonexistent_property(self):
        filepath = "resources/test_files/test.properties"
        properties_manager = PropertiesManager(filepath)
        with self.assertRaises(KeyError):
            properties_manager.get_property("nonexistent_property")
    

if __name__ == "__main__":
    unittest.main()