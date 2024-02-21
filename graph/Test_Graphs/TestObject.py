from pymongo import MongoClient

class TestObject:
    def __init__(self,mongostring):
        self.mongostring=mongostring

    def dbuse(self,dbname):
        self.client = MongoClient(self.mongostring)
        return self.client[dbname]


    def dbclose(self):
        self.client.close()

    def get_all_collections(self,db):
        collections = db.list_collection_names()
        # print(f"All collections in db are: \n {collections}")
        return collections

