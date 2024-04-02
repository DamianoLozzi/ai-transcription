import unittest
from utility_math import calculate_min_similarity

class TestCosineSimilarity(unittest.TestCase):
    def test_same_text(self):
        text = "This is a sample text."
        similarity_score = calculate_min_similarity(text, text)
        self.assertEqual(similarity_score, 1.0)

    def test_different_text(self):
        text1 = "This is a sample text."
        text2 = "This is another text."
        similarity_score = calculate_min_similarity(text1, text2)
        self.assertNotEqual(similarity_score, 1.0)
        self.assertGreater(similarity_score, 0.0)
        self.assertLess(similarity_score, 1.0)

    def test_empty_text(self):
        text1 = ""
        text2 = "This is a sample text."
        similarity_score = calculate_min_similarity(text1, text2)
        self.assertEqual(similarity_score, 0.0)

    def test_whitespace_text(self):
        text1 = "   "
        text2 = "This is a sample text."
        similarity_score = calculate_min_similarity(text1, text2)
        self.assertEqual(similarity_score, 0.0)

if __name__ == '__main__':
    unittest.main()