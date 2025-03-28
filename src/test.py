from utils.file_utils import load_csv
from preprocess.process_pipeline import preprocess_text_column

file_path = "data/raw/dataset.csv"

# Carrega o arquivo CSV
df = load_csv(file_path)

# Pré-processamento dos textos da coluna 'Descrição'
df = preprocess_text_column(df, 'Descrição')
