from fastapi import FastAPI, Depends, HTTPException, Header, status
import redis 
from app.infrastructure.redis_repo import RedisRepository
from app.infrastructure.mongodb_repo import MongoRepository
from app.infrastructure.viacep_api import ViaCepAPI
from app.application.service import CepService

app = FastAPI()

# Configurações para autenticação e rate limiting usando Redis para armazenar as requisições por chave de API
redis_client_auth = redis.Redis(host="redis", port=6379, db=0, decode_responses=True)
API_KEYS_VALIDAS = {"abc123", "teste456"}
RATE_LIMIT = 100 
WINDOW = 20

def verificar_rate_limit(api_key: str):
    chave = f"rate_limit:{api_key}"
    requisicoes = redis_client_auth.incr(chave)

    if requisicoes == 1:
        redis_client_auth.expire(chave, WINDOW)
    if requisicoes > RATE_LIMIT:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS, 
            detail="Limite de requisições excedido. Tente novamente em instantes."
        )

def autenticar(x_api_key: str = Header(None)):
    if x_api_key is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="API key ausente")
    if x_api_key not in API_KEYS_VALIDAS:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Chave de API inválida")
    
    verificar_rate_limit(x_api_key)
    return x_api_key

# Injeção de dependencias - instancias concretas das ferramentas (Redis, MongoDB e ViaCEP) 
redis_repo = RedisRepository()
mongo_repo = MongoRepository()
viacep_api = ViaCepAPI()


# Cache, Banco e por último API
cep_service = CepService(redis_repo, mongo_repo, viacep_api)

# Rota para consulta de CEP, protegida por autenticação e rate limiting
@app.get("/cep/{cep}")
def consultar_cep(cep: str, api_key: str = Depends(autenticar)):
    # O Controller (main) apenas chama o serviço e devolve o resultado 
    resultado = cep_service.get_address(cep) # O controller chama o serviço e devolve o resultado 
    
    if resultado["source"] == "not_found":
        raise HTTPException(status_code=404, detail="CEP não encontrado")
        
    return resultado

