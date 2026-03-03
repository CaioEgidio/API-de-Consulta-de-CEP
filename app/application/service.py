# app/application/service.py
from app.domain.models import Address

class CepService: # Serviço de Consulta de Endereço por CEP
    def __init__(self, cache, database, external_api): # Recebe as dependencias via injeção de dependencia 
        self.cache = cache # Interface para o Cache
        self.database = database # Interface para o Banco de Dados
        self.external_api = external_api # Interface para o Serviço Externo 

    def get_address(self, cep: str):  
        data = self.cache.get(cep)
        if data: 
            return {"source": "cache", "data": data}

        data = self.database.find_by_cep(cep) 
        if data:
            self.cache.save(cep, data)
            return {"source": "mongodb", "data": data}
        
        data = self.external_api.fetch(cep) 
        if data:
            self.database.save(data)
            self.cache.save(cep, data)
            return {"source": "api", "data": data}
        
        return {"source": "not_found", "data": None}  
