from pydantic import BaseModel

class Address(BaseModel):
    cep: str
    logradouro: str
    bairro: str
    localidade: str
    uf: str

