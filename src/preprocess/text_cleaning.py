import re
import spacy

# Carrega o modelo de português do SpaCy
nlp = spacy.load("pt_core_news_md")

def clean_text(text: str) -> str:
    """
    Remove caracteres especiais e normaliza o texto.
    """
    if not isinstance(text, str):
        return ""

    text = text.lower().strip()  
    text = re.sub(r'\d+', '', text)  
    text = re.sub(r'[^\w\s]', '', text)  
    text = re.sub(r'\s+', ' ', text)
    
    return text
