FROM python:3.12.7-slim

# Define o diretório de trabalho
WORKDIR /app

# Copia todos os arquivos do projeto
COPY . .

# Instala dependências
RUN pip install --upgrade pip && pip install -r requirements.txt

# Expõe a porta usada pelo app
EXPOSE 5001

# Comando para iniciar a aplicação (corrigido com caminho da pasta src)
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "5001"]
