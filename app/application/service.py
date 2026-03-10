from app.domain.models import Address

class CepService: # Serviço de Consulta de Endereço por CEP
    def __init__(self, cache, database, external_api): # Recebe as dependencias via injeção de dependencia 
        self.cache = cache # Interface para o Cache
        self.database = database # Interface para o Banco de Dados
        self.external_api = external_api # Interface para o Serviço Externo 

    def get_address(self, cep: str):  # Responsavel por orquestrar a logica de consulta de endereço por CEP
        data = self.cache.get(cep)
        if data: # Se o endereço for encontrado no cache, retorna imediatamente 
            return {"source": "cache", "data": data} 

        data = self.database.find_by_cep(cep) # Se o endereço não for encontrado no cache busca no banco 
        if data:# Se for encontrado no banco salva no cache 
            self.cache.save(cep, data)
            return {"source": "mongodb", "data": data}
        
        data = self.external_api.fetch(cep) # Se o endereço não for encontrado no banco, busca na API externa
        if data: # Se for encontrado na API externa, salva no banco e no cache 
            self.database.save(data)
            self.cache.save(cep, data)
            return {"source": "api", "data": data}
        
        return {"source": "not_found", "data": None}  # Se não for encontrado em nenhum lugar, retorna not_found
