import pandas as pd
from preprocess.text_cleaning import clean_text
from preprocess.tokenization import tokenize_text
from preprocess.stopwords import remove_stopwords
from preprocess.vectorization import vectorize_text
from preprocess.lemmatization import lemmatize_tokens
from preprocess.pos_tagging import pos_tagging
from preprocess.parsing import parse_text

def preprocess_text_column(df: pd.DataFrame, column: str):
    """
    Aplica o pré-processamento nos textos de uma coluna específica (como Título ou Descrição).
    """
    if column not in df.columns:
        print(f"Coluna {column} não encontrada no DataFrame.")
        return None

    df[column] = df[column].apply(clean_text)

    df[column + '_tokens'] = df[column].apply(tokenize_text)

    df[column + '_tokens_filtered'] = df[column + '_tokens'].apply(remove_stopwords)

    df[column + '_tokens_lemmatized'] = df[column + '_tokens_filtered'].apply(lemmatize_tokens)

    df[column + '_pos_tags'] = df[column + '_tokens_lemmatized'].apply(pos_tagging)

    df[column + '_parsed'] = df[column + '_tokens_lemmatized'].apply(parse_text)

    df[column + '_vectorized'] = df[column + '_tokens_lemmatized'].apply(vectorize_text)

    df.to_csv("Chamados_Processed.csv", sep=';', index=False)

    return df
