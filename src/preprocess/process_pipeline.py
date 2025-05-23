import pandas as pd
import json
from preprocess import clean_text, tokenize_text, remove_stopwords, vectorize_text, lemmatize_tokens, pos_tagging, parse_text, count_spelling_errors
from collections import Counter
from preprocess.cleaning import anonymize_sensitive_data  # Importar a função de anonimização
import shutil
import requests
import os

def preprocess_text_column(df: pd.DataFrame, column: str , id_gerado):
    if column not in df.columns:
        print(f"Coluna {column} não encontrada no DataFrame.")
        return None

    # Aplicar anonimização e salvar em nova coluna
    df[column + '_anon'] = df[column].apply(lambda x: anonymize_sensitive_data(x) if isinstance(x, str) else x)

    # Limpeza e processamento de texto usando a coluna anonimizada
    df[column + '_clean'] = df[column + '_anon'].apply(clean_text)
    df[column + '_tokens'] = df[column + '_clean'].apply(lambda x: tokenize_text(x) if isinstance(x, str) else [])
    df[column + '_tokens_filtered'] = df[column + '_tokens'].apply(remove_stopwords)
    df[column + '_tokens_lemmatized'] = df[column + '_tokens_filtered'].apply(lemmatize_tokens)

    # Verificação
    print(f"Tokens lematizados para a coluna {column}: {df[column + '_tokens_lemmatized']}")

    df[column + '_pos_tags'] = df[column + '_tokens_lemmatized'].apply(
        lambda x: pos_tagging(x)[0] if isinstance(x, list) and len(x) > 0 else {}
    )
    print(f"Tags POS para a coluna {column}: {df[column + '_pos_tags']}")

    df[column + '_parsed'] = df[column + '_tokens_lemmatized'].apply(parse_text)
    df[column + '_vectorized'] = df[column + '_tokens_lemmatized'].apply(vectorize_text)

    # 🔢 Estatísticas
    total_tokens = sum(len(tokens) for tokens in df[column + '_tokens_lemmatized'])
    pos_tag_counts = Counter()

    for idx, pos_tags in enumerate(df[column + '_pos_tags']):
        print(f"Verificando tags na linha {idx}: {pos_tags}")
        if isinstance(pos_tags, dict) and pos_tags:
            pos_tag_counts.update(pos_tags)

    word_count = Counter(word.lower() for tokens in df[column + '_tokens_lemmatized'] for word in tokens)
    most_common_words = word_count.most_common(10)

    all_spelling_errors = []
    total_errors = 0
    total_percent = 0.0

    for text in df[column + '_clean']:
        errors, palavras_erradas, percentual = count_spelling_errors(text)
        total_errors += errors
        total_percent += percentual
        all_spelling_errors.extend(palavras_erradas)

    word_count = Counter(all_spelling_errors)
    most_common_errors = word_count.most_common(10)
    media_erro_percentual = total_percent / len(df)

    resultado_json = {
        "total_tokens": total_tokens,
        "pos_tag_counts": dict(pos_tag_counts),
        "top_10_words": most_common_words,
        "top_10_spelling_errors": most_common_errors,
        "total_spelling_errors": total_errors,
        "percentual_medio_erros": round(media_erro_percentual, 2)
    }

    with open("resultado_pipeline.json", "w", encoding="utf-8") as f:
        json.dump(resultado_json, f, ensure_ascii=False, indent=4)

    # Exportar com a versão anonimizada visível
    df.to_csv("Chamados_Processed.csv", sep=';', index=False)
    # === 1. Caminho de destino no repositório de processamento ===
    # Ajuste conforme a estrutura real do seu projeto
    caminho_origem = "Chamados_Processed.csv"
    destino = os.path.abspath("/app/mnt/data/Chamados_Processed.csv")
    caminho_json_origem = "resultado_pipeline.json"
    destino_json = os.path.abspath("/app/mnt/data/resultado_pipeline.json")
    
    try:
        shutil.copy(caminho_json_origem, destino_json)
        print(f"Arquivo JSON copiado com sucesso para: {destino_json}")
    except Exception as e:
        print(f"Erro ao copiar o arquivo JSON: {e}")

    try:
        shutil.copy(caminho_origem, destino)
        print(f"Arquivo copiado com sucesso para: {destino}")
        print("Destino absoluto:", destino)
    except Exception as e:
        print(f"Erro ao copiar o arquivo: {e}")
        return df

    # === 2. Requisição para o dashboard (rota do processamento na porta 5004) ===
    try:
        print("chamou o dashboard pelo pre processamento")
        resposta = requests.get("http://processamento:5004/dashboard")
        if resposta.status_code == 200:
            print("Dashboard gerado com sucesso!")
            print(resposta.json())  # Mostra os dados retornados (métricas, etc)
            dashboard_data = resposta.json()

            # Caminho com o ID único
            output_dashboard_path = f"/app/mnt/data/resultado_dashboard_{id_gerado}.json"

            with open(output_dashboard_path, "w", encoding="utf-8") as f:
                json.dump(dashboard_data, f, ensure_ascii=False, indent=4)

            print(f"Dashboard salvo com sucesso em {output_dashboard_path}")
        else:
            print(f"Erro ao acessar /dashboard: {resposta.status_code}")
    except Exception as e:
        print(f"Erro na requisição para o processamento: {e}")
