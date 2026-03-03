from pymongo import MongoClient

class MongoRepository:
    def __init__(self, uri="mongodb://mongo:27017/"):
        self.client = MongoClient(uri)
        self.db = self.client["cep_db"]
        self.collection = self.db["ceps"]

    def find_by_cep(self, cep: str):
        doc = self.collection.find_one({"cep": cep})
        if doc:
            doc.pop("_id", None)
            return doc 
    
    def save(self, data: dict):

        self.collection.insert_one(data.copy())

        
