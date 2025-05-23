from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import os
import pandas as pd
import httpx
import json
import time
import asyncio
from utils.file_utils import load_csv
from preprocess.process_pipeline import preprocess_text_column

router = APIRouter()

UPLOAD_DIR = "./data/raw/"
PROCESSED_DIR = "./data/processed/"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(PROCESSED_DIR, exist_ok=True)

ID_SERVICE_URL = "http://localhost:5003"
ID_SERVICE_URL_PROCESSAMENTO = "http://localhost:5004"

async def process_pipeline(file_path: str, id_gerado: int):
    try:
        df = load_csv(file_path)
        print(f"[INFO] CSV carregado com {len(df)} linhas.")

        df = preprocess_text_column(df, 'Descrição', id_gerado)
        
        if df is None or df.empty:
            raise ValueError(f"[ERRO] O DataFrame retornado pelo preprocessamento está vazio ou inválido para o ID {id_gerado}.")

        # Verificação de erro aqui
        if df is None:
            raise ValueError("Erro: preprocess_text_column retornou None.")

        print("[INFO] DataFrame após preprocessamento:", type(df))
        processed_path = os.path.join(PROCESSED_DIR, "dataset_processado.csv")
        df.to_csv(processed_path, sep=';', index=False)
        print(f"[INFO] CSV processado salvo em {processed_path}")

        with open("resultado_pipeline.json", "r", encoding="utf-8") as json_file:
            resultado_json = json.load(json_file)

        async with httpx.AsyncClient() as client:
            await client.put(f"{ID_SERVICE_URL}/preprocessamento/{id_gerado}", json=resultado_json)

    except Exception as e:
        print(f"[ERRO] Erro ao processar o arquivo: {str(e)}")

async def background_pipeline(file_path: str, id_gerado: int):
    try:
        await process_pipeline(file_path, id_gerado)
        await send_tokenization_to_api(file_path="./data/processed/dataset_processado.csv", id_gerado=id_gerado)

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(f"{ID_SERVICE_URL_PROCESSAMENTO}/indexar/{id_gerado}")
                print(f"[INFO] Indexação finalizada com status: {response.status_code}")
        except Exception as index_error:
            print(f"[AVISO] Indexação falhou. Erro: {index_error}")

    except Exception as e:
        print(f"[ERRO] Erro na pipeline em background: {e}")

async def send_tokenization_to_api(id_gerado, file_path):
    try:
        df = load_csv(file_path)
        df = df.replace({pd.NA: None, pd.NaT: None, float('nan'): None, float('inf'): None, float('-inf'): None})
    except Exception as e:
        print(f"[ERRO] Erro ao carregar o arquivo: {e}")
        return

    print(f"[INFO] Carregando arquivo: {file_path}")
    print(f"[INFO] ID gerado: {id_gerado}")

    for index, row in df.iterrows():
        data_inicio_json = time.time()
        resultado_json = {
            "ID_geral": id_gerado,
            "Título": row.get("Título") or row.get("Nome do projeto"),
            "Tipo": row.get("Tipo"),
            "Descrição": row.get("Descrição"),
            "Solução - Solução": row.get("Solução - Solução"),
            "Descrição_tokens_filtered": row.get("Descrição_tokens_filtered"),
            "Descrição_tokens": row.get("Descrição_tokens"),
            "Localização": row.get("Localização"),
            "Elementos associados": row.get("Elementos associados"),
            "Data de abertura": row.get("Data de abertura") or row.get("Criado"),
            "Data de fechamento": row.get("Data de fechamento") or row.get("Resolvido"),
            "Tempo interno para atendimento excedido": row.get("Tempo interno para atendimento excedido"),
            "Tempo para atendimento": row.get("Tempo para atendimento"),
            "Limite do tempo interno de atendimento": row.get("Tempo interno para atendimento"),
            "ID_chamado": row.get("ID")
        }
        data_fim_json = time.time()
        print(f"[INFO] Tempo para gerar JSON: {data_fim_json - data_inicio_json:.2f}s")

        data_requisicao_json = time.time()
        async with httpx.AsyncClient() as client:
            response = await client.post(f"{ID_SERVICE_URL}/texto_limpo", json=resultado_json)
        data_fim_requisicao_json = time.time()
        print(f"[INFO] Tempo para enviar JSON: {data_fim_requisicao_json - data_requisicao_json:.2f}s")
        print(f"[INFO] Enviado ID {id_gerado}: {response.status_code}")

@router.post("/upload_csv/")
async def upload_csv(file: UploadFile = File(...)):
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Apenas arquivos .csv são permitidos.")

    try:
        async with httpx.AsyncClient() as client:
            # Gera ID
            post_response = await client.post(f"{ID_SERVICE_URL}/ids/")
            post_response.raise_for_status()

            # Busca último ID
            get_response = await client.get(f"{ID_SERVICE_URL}/ids/")
            get_response.raise_for_status()

            id_gerado = get_response.json()[-1].get('id')
            if not id_gerado:
                raise HTTPException(status_code=500, detail="Erro ao gerar ID no serviço de IDs.")

            # Salva o arquivo CSV localmente
            file_path = os.path.join(UPLOAD_DIR, file.filename)
            with open(file_path, "wb") as buffer:
                buffer.write(await file.read())

            # Aguarda o processamento completo antes de continuar
            await background_pipeline(file_path, id_gerado)

            # Busca o resultado atualizado
            final_response = await client.get(f"{ID_SERVICE_URL}/ids/{id_gerado}")
            final_response.raise_for_status()

            return final_response.json()

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao processar upload do CSV: {str(e)}")


    

@router.get("/resultado_dashboard/{id}")
def get_dashboard_result(id: int):
    # Usa variável de ambiente ou padrão local
    BASE_DASHBOARD_PATH = os.getenv("DASHBOARD_PATH", os.path.abspath("../../processamento/mnt/data"))
    path = os.path.join(BASE_DASHBOARD_PATH, f"resultado_dashboard_{id}.json")

    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data
    else:
        return JSONResponse(
            status_code=202,
            content={"mensagem": "Dashboard ainda está sendo gerado."}
        )




@router.get("/download_csv/{filename}")
async def download_csv(filename: str):
    file_path = os.path.join(UPLOAD_DIR, filename)
    if os.path.exists(file_path):
        return {"message": "Arquivo disponível!", "file_path": file_path}
    return {"error": "Arquivo não encontrado"}