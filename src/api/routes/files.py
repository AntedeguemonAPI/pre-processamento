from fastapi import APIRouter, UploadFile, File, HTTPException
import os
import pandas as pd
import requests
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

        requests.put(f"{ID_SERVICE_URL}/preprocessamento/{id_gerado}", json=resultado_json)
    except Exception as e:
        print(f"Erro ao processar o arquivo: {str(e)}")

@router.post("/upload_csv/")
async def upload_csv(file: UploadFile = File(...)):
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Apenas arquivos .csv são permitidos.")

    try:
        post_response = requests.post(f"{ID_SERVICE_URL}/ids")
        post_response.raise_for_status()
        
        get_response = requests.get(f"{ID_SERVICE_URL}/ids")
        get_response.raise_for_status()
        
        id_gerado = get_response.json()[-1].get('id')
        if not id_gerado:
            raise HTTPException(status_code=500, detail="Erro ao gerar ID no serviço de IDs.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao se conectar com o serviço de IDs: {str(e)}")
    
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())
    
    asyncio.create_task(process_pipeline(file_path, id_gerado))
    
    try:
        final_response = requests.get(f"{ID_SERVICE_URL}/ids/{id_gerado}")
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
