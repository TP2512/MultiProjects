from pymongo import MongoClient


class MongoDBConnection:
    def __init__(self, db_name, collection_name):
        self.client = MongoClient("mongodb://localhost:27017/")
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def get_collection(self):
        return self.collection
