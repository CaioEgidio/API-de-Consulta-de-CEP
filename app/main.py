from fastapi import FastAPI, HTTPException
import requests
import redis
from pymongo import MongoClient
import json

app = FastAPI()

# Conexão com Redis
redis_client = redis.Redis(host="redis", port=6379, db=0,decode_responses=True)

# Conexão com MongoDB
mongo_client = MongoClient("mongodb://mongo:27017/")
db = mongo_client["cep_db"] # Nome do banco de dados
mongo_collection = db["ceps"]

URL = "https://viacep.com.br/ws/"
TTL = 86400  # 24 horas

@app.get("/cep/{cep}")
def consultar_cep(cep: str):
    # 1. Tenta buscar no REDIS (Cache)
    cached = redis_client.get(cep)# Verifica se o CEP esta no cache
    if cached:
        return {"source": "cache", "data": json.loads(cached)}# Retorna o valor do cache

    # 2. Tenta buscar no MONGODB
    doc = mongo_collection.find_one({"cep": cep})
    if doc: # Se encontrou no MongoDB
        doc.pop("_id", None)  # Remove o ObjectId para não quebrar o JSON
        redis_client.setex(cep, TTL, json.dumps(doc)) # Atualiza o cache no Redis
        return {"source": "mongodb", "data": doc}# Retorna o documento encontrado

    # 3. Tenta buscar na API EXTERNA (ViaCEP)
    try:  
        response = requests.get(f"{URL}{cep}/json", timeout=10)
        response.raise_for_status()
        data = response.json()
    except Exception:  
        raise HTTPException(status_code=502, detail="Erro ao consultar serviço externo") 

    if "erro" in data:
        raise HTTPException(status_code=404, detail="CEP não encontrado")

    # 4. SALVAR NO MONGO E NO REDIS
    # inserimos uma cópia ou limpamos o _id depois
    mongo_collection.insert_one(data.copy()) # insere os dados no MongoDB
    data.pop("_id", None) # Garante que o _id gerado pelo mongo não vá para o Redis/Resposta
    
    redis_client.setex(cep, TTL, json.dumps(data))

    return {"source": "api", "data": data} # Retorna os dados da API externa 
# codigo 404: não encontrado
# raise interrompe o programa quando um erro acontece 
