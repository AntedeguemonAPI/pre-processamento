from fastapi import APIRouter, UploadFile, File, HTTPException
import os
import pandas as pd
import httpx  # Use httpx instead of requests
import json
import asyncio
from utils.file_utils import load_csv
from preprocess.process_pipeline import preprocess_text_column

router = APIRouter()

UPLOAD_DIR = "./data/raw/"
PROCESSED_DIR = "./data/processed/"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(PROCESSED_DIR, exist_ok=True)

ID_SERVICE_URL = "http://banco-de-dados:5003"

async def process_pipeline(file_path: str, id_gerado: int):
    try:
        df = load_csv(file_path)
        df = preprocess_text_column(df, 'Descrição')
        processed_path = os.path.join(PROCESSED_DIR, "dataset_processado.csv")
        df.to_csv(processed_path, sep=';', index=False)

        with open("resultado_pipeline.json", "r", encoding="utf-8") as json_file:
            resultado_json = json.load(json_file)
        
        async with httpx.AsyncClient() as client:  # Use async with httpx
            await client.put(f"{ID_SERVICE_URL}/preprocessamento/{id_gerado}", json=resultado_json)
    except Exception as e:
        print(f"Erro ao processar o arquivo: {str(e)}")

async def send_tokenization_to_api(id_gerado, file_path):
    df = load_csv(file_path)
    df = df.replace({pd.NA: None, pd.NaT: None, float('nan'): None, float('inf'): None, float('-inf'): None})

    print(f"Carregando arquivo: {file_path}")
    print(f"ID gerado: {id_gerado}")
    for index, row in df.iterrows():
        resultado_json = {
            "ID_geral": id_gerado,
            "Descrição_tokens_filtered": row["Descrição_tokens_filtered"],
            "Descrição_tokens": row["Descrição_tokens"],
            "Solução - Solução": row["Solução - Solução"],
            "Descrição": row["Descrição"],
            "Data de abertura": row["Data de abertura"],
            "Data de fechamento": row["Data de fechamento"]
        }

        async with httpx.AsyncClient() as client:  # Use async with httpx
            response = await client.post(
                f"{ID_SERVICE_URL}/texto_limpo",
                json=resultado_json
            )

        print(f"Enviado ID {id_gerado}: {response.status_code}")

@router.post("/upload_csv/")
async def upload_csv(file: UploadFile = File(...)):
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Apenas arquivos .csv são permitidos.")

    try:
        async with httpx.AsyncClient() as client:  # Use httpx for async HTTP calls
            post_response = await client.post(f"{ID_SERVICE_URL}/ids")
            post_response.raise_for_status()

            get_response = await client.get(f"{ID_SERVICE_URL}/ids")
            get_response.raise_for_status()
            
            id_gerado = get_response.json()[-1].get('id')
            if not id_gerado:
                raise HTTPException(status_code=500, detail="Erro ao gerar ID no serviço de IDs.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao se conectar com o serviço de IDs: {str(e)}")
    
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())
    
    # Replace requests with async task calls
    asyncio.create_task(process_pipeline(file_path, id_gerado))
    asyncio.create_task(send_tokenization_to_api(file_path="./data/processed/dataset_processado.csv" ,id_gerado=id_gerado))
    asyncio.create_task(httpx.AsyncClient().post(f"http://processamento:5004/indexar/{id_gerado}"))

    try:
        async with httpx.AsyncClient() as client:  # Use httpx for async HTTP calls
            final_response = await client.get(f"{ID_SERVICE_URL}/ids/{id_gerado}")
            final_response.raise_for_status()
            return final_response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar dados do ID gerado: {str(e)}")


@router.get("/download_csv/{filename}")
async def download_csv(filename: str):
    file_path = os.path.join(UPLOAD_DIR, filename)
    if os.path.exists(file_path):
        return {"message": "Arquivo disponível!", "file_path": file_path}
    return {"error": "Arquivo não encontrado"}