from fastapi import FastAPI
from api.routes import files
import uvicorn

app = FastAPI()

# Incluindo as rotas de upload/download
app.include_router(files.router, prefix="/files", tags=["Arquivos"])

@app.get("/")
async def root():
    return {"message": "API de Pré-processamento PLN está rodando!"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=5001, reload=True)