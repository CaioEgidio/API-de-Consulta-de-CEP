from fastapi import FastAPI, HTTPException
import requests

app = FastAPI()

URL = "https://viacep.com.br/ws/"   

@app.get("/cep/{cep}")
def consultar_cep(cep: str): #string recebida pela URL
    response = requests.get(f"{URL}{cep}/json", timeout=60) #Faz uma requisição pro ViaCEP e espera no máximo 60 segundos.

    if response.status_code != 200: # Checa se a requisição deu certo
        raise HTTPException(status_code=404, detail="Erro ao consultar CEP")

    data = response.json() # Converte a resposta do ViaCEP em json

    if "erro" in data:# verifica se existe um a palavra chave "erro" dentro do json
        raise HTTPException(status_code=404, detail="CEP não encontrado")

    return data

# codigo 404: não encontrado
# raise interrompe o programa quando um erro acontece 
