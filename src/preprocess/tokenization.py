import spacy

# Carrega o modelo SpaCy
nlp = spacy.load("pt_core_news_md")

def tokenize_text(text):
    """
    Tokeniza uma string individual usando SpaCy.
    """
    if not text or not isinstance(text, str):  # Verifica se o texto é válido
        return []

    doc = nlp(text)
    tokens = [token.text for token in doc if not token.is_punct]


    return tokens
