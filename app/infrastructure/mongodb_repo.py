from pymongo import MongoClient

class MongoRepository: 
    def __init__(self, uri="mongodb://mongo:27017/"): # Conexão com o MongoDB usando a URI fornecida
        self.client = MongoClient(uri) # Cria uma instancia do cliente MongoDB
        self.db = self.client["cep_db"] # Acessa o banco de dados "cep_db" sera criado se não existir
        self.collection = self.db["ceps"] # Acessa a coleção "ceps" sera criada se não existir 

    def find_by_cep(self, cep: str): # Busca um documento no MongoDB usando o CEP como Filtro
        doc = self.collection.find_one({"cep": cep})
        if doc: # Se um documento for encontrado, remove o campo _id (gerado pelo MongoDB)
            doc.pop("_id", None)
            return doc 
    
    def save(self, data: dict): # Salva um documento no MongoDB, usando uma copia dos dados para evitar mutações 

        self.collection.insert_one(data.copy()) # Insere o documento na coleção "ceps" do banco de dados "cep_db"

        

        
