from sklearn.feature_extraction.text import TfidfVectorizer
from gensim.models import Word2Vec
from sentence_transformers import SentenceTransformer
import numpy as np

def convert_text_to_vectors(text_data, method="tfidf"):
    """Convertit un dictionnaire de textes en vecteurs"""
    table_names = list(text_data.keys())
    texts = list(text_data.values())

    if method == "tfidf":
        vectorizer = TfidfVectorizer()
        vectors = vectorizer.fit_transform(texts).toarray()

    elif method == "word2vec":
        tokenized_texts = [text.split() for text in texts]
        w2v_model = Word2Vec(sentences=tokenized_texts, vector_size=100, window=5, min_count=1, workers=4)
        vectors = [np.mean([w2v_model.wv[word] for word in text.split() if word in w2v_model.wv], axis=0)
                   if text else np.zeros(100) for text in texts]

    elif method == "bert":
        model = SentenceTransformer("all-MiniLM-L6-v2")
        vectors = model.encode(texts)

    else:
        raise ValueError("Méthode non supportée. Choisissez entre 'tfidf', 'word2vec' ou 'bert'.")

    return {table: vector for table, vector in zip(table_names, vectors)}
