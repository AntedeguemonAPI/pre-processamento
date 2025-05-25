import spacy
import re

nlp = spacy.load("pt_core_news_md")

def anonymize_sensitive_data(text: str) -> str:
    if not isinstance(text, str):
        return text

    # Detecta entidades
    doc = nlp(text)

    # Substitui nomes próprios (pessoas)
    anonymized_text = text
    for ent in doc.ents:
        if ent.label_ == "PER":
            anonymized_text = anonymized_text.replace(ent.text, "***NOME***")

    # Substitui apenas CPFs no formato xxx.xxx.xxx-xx
    cpf_pattern = r"\b\d{3}\.\d{3}\.\d{3}-\d{2}\b"
    anonymized_text = re.sub(cpf_pattern, "***CPF***", anonymized_text)

    return anonymized_text
