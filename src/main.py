from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import files
import uvicorn

app = FastAPI()

# Configuração do CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluindo as rotas de upload/download
app.include_router(files.router, prefix="/files", tags=["Arquivos"])

@app.get("/")
async def root():
    return {"message": "API de Pré-processamento PLN está rodando!"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=5001, reload=True)
