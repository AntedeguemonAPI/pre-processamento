import spacy

# Carrega o modelo de português
nlp = spacy.load("pt_core_news_sm")

def pos_tagging(text: str) -> list:
    """
    Realiza a rotulação gramatical (POS Tagging) utilizando o SpaCy.
    Retorna uma lista de tuplas (token, tag).
    """
    if not isinstance(text, str):
        return []

    doc = nlp(text)
    return [(token.text, token.pos_) for token in doc]  # (token, POS tag)
