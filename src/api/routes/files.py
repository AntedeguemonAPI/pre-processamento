from fastapi import APIRouter, UploadFile, File, HTTPException,FastAPI
import os
import pandas as pd
import httpx  # Use httpx instead of requests
import json
import time
import httpx
import asyncio
from utils.file_utils import load_csv
from preprocess.process_pipeline import preprocess_text_column

from src.api.routes import files 



router = APIRouter()

UPLOAD_DIR = "./data/raw/"
PROCESSED_DIR = "./data/processed/"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(PROCESSED_DIR, exist_ok=True)

ID_SERVICE_URL = "http://banco-de-dados:5003"
ID_SERVICE_URL_PROCESSAMENTO = "http://processamento:5004"

async def process_pipeline(file_path: str, id_gerado: int):
    try:
        df = load_csv(file_path)
        df = preprocess_text_column(df, 'Descrição',id_gerado)
        processed_path = os.path.join(PROCESSED_DIR, "dataset_processado.csv")
        df.to_csv(processed_path, sep=';', index=False)

        with open("resultado_pipeline.json", "r", encoding="utf-8") as json_file:
            resultado_json = json.load(json_file)
        
        async with httpx.AsyncClient() as client:  # Use async with httpx
            await client.put(f"{ID_SERVICE_URL}/preprocessamento/{id_gerado}", json=resultado_json)
    except Exception as e:
        print(f"Erro ao processar o arquivo: {str(e)}")

async def background_pipeline(file_path: str, id_gerado: int):
    try:
        await process_pipeline(file_path, id_gerado)
        await send_tokenization_to_api(file_path="./data/processed/dataset_processado.csv", id_gerado=id_gerado)
        
        # Tenta fazer a requisição de indexação, mas não interrompe o processo se falhar
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(f"{ID_SERVICE_URL_PROCESSAMENTO}/indexar/{id_gerado}")
                print(f"Indexação finalizada com status: {response.status_code}")
        except Exception as index_error:
            print(f"Indexação falhou, mas o processo continuará. Erro: {index_error}")

    except Exception as e:
        print(f"Erro na pipeline em background: {e}")

async def send_tokenization_to_api(id_gerado, file_path):
    df = load_csv(file_path)
    df = df.replace({pd.NA: None, pd.NaT: None, float('nan'): None, float('inf'): None, float('-inf'): None})

    print(f"Carregando arquivo: {file_path}")
    print(f"ID gerado: {id_gerado}")
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
        print(f"Tempo de execução para gerar JSON: {data_fim_json - data_inicio_json:.2f} segundos")

        data_requisicao_json = time.time()
        async with httpx.AsyncClient() as client:  
            response = await client.post(
                f"{ID_SERVICE_URL}/texto_limpo",
                json=resultado_json
            )
        data_fim_requisicao_json = time.time()
        print(f"Tempo de execução para enviar JSON: {data_fim_requisicao_json - data_requisicao_json:.2f} segundos")

        print(f"Enviado ID {id_gerado}: {response.status_code}")

@router.post("/upload_csv/")
async def upload_csv(file: UploadFile = File(...)):
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Apenas arquivos .csv são permitidos.")

    try:
        async with httpx.AsyncClient() as client:
            # POST para gerar o ID
            post_response = await client.post(f"{ID_SERVICE_URL}/ids/")
            post_response.raise_for_status()

            # GET para recuperar o último ID
            get_response = await client.get(f"{ID_SERVICE_URL}/ids/")
            get_response.raise_for_status()

            id_gerado = get_response.json()[-1].get('id')
            if not id_gerado:
                raise HTTPException(status_code=500, detail="Erro ao gerar ID no serviço de IDs.")

            # Salva o arquivo
            file_path = os.path.join(UPLOAD_DIR, file.filename)
            with open(file_path, "wb") as buffer:
                buffer.write(await file.read())

            # Inicia o pipeline
            asyncio.create_task(background_pipeline(file_path, id_gerado))

            # Requisição final dentro do mesmo cliente
            final_response = await client.get(f"{ID_SERVICE_URL}/ids/{id_gerado}")
            final_response.raise_for_status()
            return final_response.json()

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao processar upload do CSV: {str(e)}")
    

@router.get("/resultado_dashboard/{id}")
def get_dashboard_result(id: int):
    path = f"/app/mnt/data/resultado_dashboard_{id}.json"

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