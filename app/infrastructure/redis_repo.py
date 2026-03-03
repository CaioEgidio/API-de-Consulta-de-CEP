import redis
import json

class RedisRepository:
    def __init__(self, host="redis", port=6379):
        self.redis_client = redis.Redis(host=host, port=port, db=0, decode_responses=True)
        self.ttl = 86400 # 24 horas

    def get(self, cep: str): # Busca o valor no Redis usando o CEP como chave
        data = self.redis_client.get(cep)
        return json.loads(data) if data else None # Se o valor existir, mostra o json decodificado, se não mostra none
        
    def save(self, cep: str, data: dict):# Salva o valor no Redis com o CEP como chave e define um tempo de expiração TTL
        self.redis_client.setex(cep, self.ttl, json.dumps(data))

