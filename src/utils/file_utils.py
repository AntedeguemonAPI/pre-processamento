import pandas as pd

def load_csv(file_path: str):
    """
    Carrega o arquivo CSV no formato específico e retorna como DataFrame.
    """
    try:
        df = pd.read_csv(file_path, sep=';', encoding='utf-8')
        return df
    except Exception as e:
        print(f"Erro ao carregar o arquivo: {e}")
        return None