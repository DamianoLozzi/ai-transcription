from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from utility_log import LogManager
from sklearn.feature_extraction.text import TfidfVectorizer

import logging
import numpy as np
import concurrent.futures


lm = LogManager("whisper_logger", logging.INFO)

def calculate_cosine_similarity(text1, text2):
    try:
        lm.starting_process("utility_math", "calculate_cosine_similarity")
        # Text preprocessing
        text1 = text1.lower()  # Convert to lowercase
        text2 = text2.lower()
        
        # TF-IDF Vectorization
        vectorizer = TfidfVectorizer()
        vectorized_text = vectorizer.fit_transform([text1, text2])
        vectorized_text = vectorized_text.toarray()
        
        # Calculate cosine similarity
        similarity_score = cosine_similarity(vectorized_text[0].reshape(1, -1), vectorized_text[1].reshape(1, -1))[0][0]
        
        # Ensure similarity score is between 0 and 1
        similarity_score = np.clip(similarity_score, 0, 1)
        lm.ending_process("utility_math", "calculate_cosine_similarity", True, f"Similarity score: {similarity_score}")
        return similarity_score
    except Exception as e:
        lm.ending_process("utility_math", "calculate_cosine_similarity", False, f"Error calculating cosine similarity: {str(e)}")
        raise ValueError(f"Error calculating cosine similarity: {str(e)}")

def calculate_jaccard_similarity(text1, text2):
    try:
        lm.starting_process("utility_math", "calculate_jaccard_similarity")
        # Text preprocessing
        text1 = set(text1.lower().split())  # Convert to lowercase and split into tokens
        text2 = set(text2.lower().split())

        # Calculate Jaccard similarity
        intersection = len(text1.intersection(text2))
        union = len(text1.union(text2))
        jaccard_similarity = intersection / union if union != 0 else 0  # Avoid division by zero

        lm.ending_process("utility_math", "calculate_jaccard_similarity", True, f"Jaccard similarity: {jaccard_similarity}")
        return jaccard_similarity
    except Exception as e:
        lm.ending_process("utility_math", "calculate_jaccard_similarity", False, f"Error calculating Jaccard similarity: {str(e)}")
        raise ValueError(f"Error calculating Jaccard similarity: {str(e)}")
    
def calculate_min_similarity(text1, text2):
    try:
        lm.starting_process("utility_math", "calculate_min_similarity")
        # Text preprocessing
        text1 = remove_punctuation(text1.lower())  # Convert to lowercase
        text2 = remove_punctuation(text2.lower())
        
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future1 = executor.submit(calculate_cosine_similarity, text1, text2)
            future2 = executor.submit(calculate_jaccard_similarity, text1, text2)
            score1 = future1.result()
            score2 = future2.result()
            lm.ending_process("utility_math", "calculate_min_similarity", True, f"Min similarity: {min(score1, score2)}")
            
            return min(score1, score2)        
    except Exception as e:
        lm.ending_process("utility_math", "calculate_min_similarity", False, f"Error calculating min similarity: {str(e)}")
        raise ValueError(f"Error calculating min similarity: {str(e)}")
    
def remove_punctuation(text):
    try:
        lm.starting_process("utility_math", "remove_punctuation")
        # Remove punctuation
        text = ''.join([char for char in text if char.isalnum() or char.isspace()])
        lm.ending_process("utility_math", "remove_punctuation", True, f"Text without punctuation: {text}")
        return text
    except Exception as e:
        lm.ending_process("utility_math", "remove_punctuation", False, f"Error removing punctuation: {str(e)}")
        raise ValueError(f"Error removing punctuation: {str(e)}")
