import requests
from fastapi import HTTPException

class ViaCepAPI:
    def __init__(self): # URL base da API ViaCEP
        self.url = "https://viacep.com.br/ws/"

    def fetch(self, cep: str): # Método para buscar o endereço pelo CEP
        try: # Realiza a requisição para a API ViaCEP
            response = requests.get(f"{self.url}{cep}/json", timeout=5)
            response.raise_for_status()
            data = response.json()

            if "erro" in data: # Se a resposta contiver erro, significa que o CEP não foi econtrado
                return None
            return data 
        except Exception: # Em caso de erro na requisição, lança um excecão HTTP 503 
            raise HTTPException(status_code=503, detail="Erro ao consultar serviço externo")
        
        