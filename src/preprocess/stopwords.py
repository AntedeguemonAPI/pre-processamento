import spacy

# Carrega o modelo de português
nlp = spacy.load("pt_core_news_sm")

def remove_stopwords(tokens: list) -> list:
    """
    Remove stopwords da lista de tokens.
    """
    if not isinstance(tokens, list):
        return []

    return [token for token in tokens if token.lower() not in nlp.Defaults.stop_words]
