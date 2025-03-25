import spacy
import numpy as np


nlp = spacy.load("pt_core_news_sm")

def vectorize_text(text: str) -> np.ndarray:
    """
    Retorna o vetor do texto usando embeddings do SpaCy.
    """
    if not isinstance(text, str):
        return np.zeros((300,)) 

    doc = nlp(text)
    return doc.vector  
