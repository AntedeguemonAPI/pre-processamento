import spacy

nlp = spacy.load("pt_core_news_md")

# Lista de palavras comuns que não devem ser consideradas erros
stop_words = {"de", "o", "a", "que", "para", "do", "da", "no", "na", "em", "e", "os", "as", "como", "com", "sem"}

def count_spelling_errors(text: str):
    """
    Detecta e conta possíveis erros de português, excluindo palavras comuns.
    """
    if not isinstance(text, str):
        return 0, []

    doc = nlp(text)
    erros = 0
    palavras_erradas = []

    for token in doc:
        # Ignora palavras comuns e verifica se a palavra é OOV
        if token.is_oov and token.text.lower() not in stop_words:
            erros += 1
            palavras_erradas.append(token.text)  # Adiciona a palavra errada

    return erros, palavras_erradas
