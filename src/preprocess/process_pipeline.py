import pandas as pd
from preprocess import clean_text, tokenize_text, remove_stopwords, vectorize_text, lemmatize_tokens, pos_tagging, parse_text


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
