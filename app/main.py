from fastapi import FastAPI, HTTPException
import requests
import redis
from pymongo import MongoClient
import json
from fastapi import FastAPI, Header, HTTPException, status, Depends


app = FastAPI()


API_KEYS_VALIDAS = {"abc123", "teste456"}

# função para validar a API key, garante que o campo não esta vazio, se tiver algo continua 
def obter_api_key(x_api_key: str | None) -> str: # Verifica se a API key esta presente no header
    if x_api_key is None: # Se a API key não for fornecida 
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail= "API key ausente")# Lança uma exceção HTTP
    return x_api_key # Retorna a API key para ser validada a seguir 


# Função de que valida a API key usando o Header, recebe a string que já foi capturada e a compara com a lista de chaves
def validar_api_key(api_key: str) -> None: # Verifica se a API key é valida 
    if api_key not in API_KEYS_VALIDAS:# se a chave não for valida 
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="API key invalida")
    
# Função de dependencia que combina a obtenção e validação da API key, usa as rotas do FastAPI (usando o Depends) 
def autenticar(x_api_key: str = Header(None)) -> None: 
    api_key = obter_api_key(x_api_key) # Obtem a API key do header e valida
    validar_api_key(api_key) 
    

# Conexão com Redis
redis_client = redis.Redis(host="redis", port=6379, db=0,decode_responses=True)# traduz os bytes para string automaticamente


# Conexão com MongoDB
mongo_client = MongoClient("mongodb://mongo:27017/")
db = mongo_client["cep_db"] # Nome do banco de dados
mongo_collection = db["ceps"] # nome da coleção 

URL = "https://viacep.com.br/ws/"
TTL = 86400  # 24 horas 60*60*24 

@app.get("/cep/{cep}")
def consultar_cep(cep: str, _: None = Depends(autenticar)):
    # 1. Tenta buscar no REDIS (Cache)
    cached = redis_client.get(cep)# Verifica se o CEP esta no cache
    if cached:# se econtrou no cache
        return {"source": "cache", "data": json.loads(cached)}# Retorna o valor do cache

    # 2. Tenta buscar no MONGODB
    doc = mongo_collection.find_one({"cep": cep})
    if doc: # Se encontrou no MongoDB
        doc.pop("_id", None)  # Remove o ObjectId para não quebrar o JSON
        redis_client.setex(cep, TTL, json.dumps(doc)) # Atualiza o cache no Redis json.dumps transforma o dicionario em string 
        return {"source": "mongodb", "data": doc}# Retorna o documento encontrado

    # 3. Tenta buscar na API EXTERNA (ViaCEP)
    try:  
        response = requests.get(f"{URL}{cep}/json", timeout=10) # faz a requisição para a API externa 
        response.raise_for_status()# verifica se a resposta foi bem sucedida 
        data = response.json() 
    except Exception:# Se der erro na requisição, except significa exceção
        raise HTTPException(status_code=502, detail="Erro ao consultar serviço externo") 

    if "erro" in data:
        raise HTTPException(status_code=404, detail="CEP não encontrado")

    # 4. Salva no MongoDB e no Redis
    # inserimos uma cópia ou limpamos o _id depois
    mongo_collection.insert_one(data.copy()) # insere os dados no MongoDB 
    data.pop("_id", None) # Garante que o _id gerado pelo mongo não vá para o Redis/Resposta 
    
    redis_client.setex(cep, TTL, json.dumps(data)) # Salva o dado no cache do Redis com TTL 


    return {"source": "api", "data": data} # Retorna os dados da API externa, se ele nao tiver no cache nem no mongo
# codigo 404: não encontrado
# raise alerta e interrompe o programa quando um erro acontece
# Try except: tenta fazer algo, se der erro, faz outra coisa 
# raise HTTPException: lança uma exceção HTTP com o codigo e a mensagem fornecidos
#-> str	Promete devolver um texto.	return "Chave Válida"
#-> int	Promete devolver um número inteiro.	return 200
#-> None Não devolve nada.	Apenas executa uma ação ou validação.
