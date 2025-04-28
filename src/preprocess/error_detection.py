import spacy

nlp = spacy.load("pt_core_news_md")

stop_words = {"de", "o", "a", "que", "para", "do", "da", "no", "na", "em", "e", "os", "as", "como", "com", "sem"}

palavras_validas_customizadas = {
    "thaylla", "layla", "ingridy", "gilmaria", "araguaína", "laryssa", "danyelly", "ronice",
    "sienge", "supmed", "hgp", "lacen", "microcontroladora", "marddie"
}

def parece_nome_ou_sigla(palavra: str) -> bool:
    return (
        palavra.isupper() or
        palavra[0].isupper() or
        any(char.isdigit() for char in palavra) or
        len(palavra) > 20 or
        "." in palavra or "@" in palavra
    )

def count_spelling_errors(text: str):
    if not isinstance(text, str):
        return 0, [], 0.0

    doc = nlp(text)
    total_tokens = len([token for token in doc if not token.is_punct and not token.is_space])
    erros = 0
    palavras_erradas = []

    for token in doc:
        palavra = token.text.lower()

        if (
            token.is_oov and
            palavra not in stop_words and
            palavra not in palavras_validas_customizadas and
            not parece_nome_ou_sigla(token.text) and
            token.pos_ != "PROPN" and
            token.ent_type_ != "PER"
        ):
            erros += 1
            palavras_erradas.append(token.text)

    porcentagem_erro = (erros / total_tokens) * 100 if total_tokens > 0 else 0.0

    return erros, palavras_erradas, porcentagem_erro
