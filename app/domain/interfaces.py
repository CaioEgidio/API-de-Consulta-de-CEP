# app/domain/interfaces.py
from abc import ABC, abstractmethod

class ICacheRepository(ABC): # Interface para o Cache (Redis)
    @abstractmethod 
    def get(self, key: str): pass # pass signica que o metodo é abstrato  
    @abstractmethod
    def save(self, key: str, value: dict): pass 

class IDatabaseRepository(ABC): # Interface para o Banco de Dados (MongoDB)
    @abstractmethod
    def find_by_cep(self, cep: str): pass
    @abstractmethod
    def save(self, data: dict): pass

class IExternalApi(ABC): # Interface para o Serviço Externo (ViaCEP)
    @abstractmethod
    def fetch(self, cep: str): pass
    