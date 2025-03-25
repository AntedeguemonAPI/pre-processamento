import spacy

# Carrega o modelo de português
nlp = spacy.load("pt_core_news_sm")

def parse_text(text: str):
    """
    Realiza a análise sintática (Parsing) de um texto utilizando o SpaCy.
    Retorna a árvore de dependência da frase.
    """
    if not isinstance(text, str):
        return None

    doc = nlp(text)

    # Exemplo de como extrair as dependências de cada token
    parsed_info = []
    for token in doc:
        parsed_info.append({
            "token": token.text,
            "dep": token.dep_,
            "head": token.head.text
        })
    
    return parsed_info
