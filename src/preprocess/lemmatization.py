import spacy

# Carrega o modelo de português
nlp = spacy.load("pt_core_news_sm")

def lemmatize_tokens(tokens: list) -> list:
    """
    Aplica lematização nos tokens utilizando o SpaCy.
    """
    if not isinstance(tokens, list):
        return []

    doc = nlp(" ".join(tokens))  # Recria o texto a partir dos tokens
    return [token.lemma_ for token in doc]