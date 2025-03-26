import spacy
from collections import Counter

# Carrega o modelo SpaCy
nlp = spacy.load("pt_core_news_md")

def pos_tagging(tokens):
    """
    Aplica POS tagging nos tokens e conta a quantidade de vezes que cada tag aparece.
    """
    # Inicializa o contador para as tags
    tag_counts = Counter()
    
    # Verifica se os tokens são válidos
    if not tokens or not isinstance(tokens, list):
        return {}, "Lista de tokens inválida ou vazia."

    # Processa cada token com SpaCy para obter a tag de POS
    for token in tokens:
        # Aplica o processamento no token
        doc = nlp(token)
        for word in doc:
            if word.pos_ != "PUNCT" and word.text.strip():  # Ignora pontuação e tokens vazios
                # Atualiza a contagem da tag POS
                tag_counts.update([word.pos_])

    return tag_counts, f"Tags encontradas: {tag_counts}"
