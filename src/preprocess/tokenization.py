import spacy

# Carrega o modelo de português
nlp = spacy.load("pt_core_news_sm")

def tokenize_text(text: str) -> list:
    """
    Tokeniza o texto usando SpaCy.
    """
    if not isinstance(text, str):
        return []

    doc = nlp(text)
    return [token.text for token in doc if not token.is_punct]
