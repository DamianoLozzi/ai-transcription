from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
 

def calculate_cosine_similarity(text1, text2):
    # Create CountVectorizer object
    vectorizer = CountVectorizer()

    # Fit and transform the text data
    vectorized_text = vectorizer.fit_transform([text1, text2])

    # Convert the sparse matrix to numpy array
    vectorized_text = vectorized_text.toarray()

    # Calculate cosine similarity
    similarity_score = cosine_similarity(vectorized_text[0].reshape(1, -1), vectorized_text[1].reshape(1, -1))[0][0]

    # Return the similarity score
    return similarity_score


