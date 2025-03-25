from fastapi import APIRouter, UploadFile, File
import shutil
import os

router = APIRouter()

UPLOAD_DIR = "data/raw/"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload_csv/")
async def upload_csv(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"message": "Arquivo enviado com sucesso!", "file_path": file_path}

@router.get("/download_csv/{filename}")
async def download_csv(filename: str):
    file_path = os.path.join(UPLOAD_DIR, filename)
    if os.path.exists(file_path):
        return {"message": "Arquivo disponível!", "file_path": file_path}
    return {"error": "Arquivo não encontrado"}
