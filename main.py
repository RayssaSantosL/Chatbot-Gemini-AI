# main.py (VERSÃO DE TESTE SIMPLIFICADA)
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "Hello from Render!"}