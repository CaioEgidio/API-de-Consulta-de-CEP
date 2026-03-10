from pydantic import BaseModel

class Address(BaseModel):
    cep: str
    logradouro: str
    bairro: str
    localidade: str
    uf: str

# uso o pydantic para criar um modelo de dados para o endereço
# isso ajuda a garantir que os dados estejam no formato correto e ajuda na validação

