from fastapi import FastAPI
from src.api.routes import files

app = FastAPI()

# Incluindo as rotas de upload/download
app.include_router(files.router, prefix="/files", tags=["Arquivos"])

@app.get("/")
async def root():
    return {"message": "API de Pré-processamento PLN está rodando!"}
