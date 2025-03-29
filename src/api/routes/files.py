from fastapi import APIRouter, UploadFile, File, HTTPException
import os
import pandas as pd
import requests
import json
from utils.file_utils import load_csv
from preprocess.process_pipeline import preprocess_text_column

router = APIRouter()

UPLOAD_DIR = "./data/raw/"
PROCESSED_DIR = "./data/processed/"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(PROCESSED_DIR, exist_ok=True)

ID_SERVICE_URL = "http://127.0.0.1:5003"

@router.post("/upload_csv/")
async def upload_csv(file: UploadFile = File(...)):
    # Verifica se o arquivo é .csv
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Apenas arquivos .csv são permitidos.")

    # Faz POST na rota /ids para gerar um novo ID
    try:
        post_response = requests.post(f"{ID_SERVICE_URL}/ids")
        post_response.raise_for_status()

        # Depois faz GET para buscar o último ID gerado
        get_response = requests.get(f"{ID_SERVICE_URL}/ids")
        get_response.raise_for_status()

        # Extrai o último ID gerado
        id_gerado = get_response.json()[-1].get('id')  # Pega o último ID da lista
        if not id_gerado:
            raise HTTPException(status_code=500, detail="Erro ao gerar ID no serviço de IDs.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao se conectar com o serviço de IDs: {str(e)}")

    # Caminho para salvar o arquivo
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    
    # Salva o arquivo na pasta de upload
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    # Carrega e processa o arquivo na pipeline
    try:
        df = load_csv(file_path)
        df = preprocess_text_column(df, 'Descrição')

        # Salva o resultado na pasta de arquivos processados
        processed_path = os.path.join(PROCESSED_DIR, "dataset_processado.csv")
        df.to_csv(processed_path, sep=';', index=False)

        # Carrega o JSON gerado na pipeline
        with open("resultado_pipeline.json", "r", encoding="utf-8") as json_file:
            resultado_json = json.load(json_file)

        # Envia o JSON para a rota PUT
        try:
            put_response = requests.put(f"{ID_SERVICE_URL}/preprocessamento/{id_gerado}", json=resultado_json)
            put_response.raise_for_status()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro ao enviar dados para o serviço de IDs: {str(e)}")

        return {
            "message": "Arquivo processado com sucesso!",
            "original_file_path": file_path,
            "processed_file_path": processed_path,
            "id_gerado": id_gerado
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao processar o arquivo: {str(e)}")

@router.get("/download_csv/{filename}")
async def download_csv(filename: str):
    file_path = os.path.join(UPLOAD_DIR, filename)
    if os.path.exists(file_path):
        return {"message": "Arquivo disponível!", "file_path": file_path}
    return {"error": "Arquivo não encontrado"}
