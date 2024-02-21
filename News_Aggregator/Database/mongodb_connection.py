from pymongo import MongoClient

db_name="news_articles"
CONNECTION_STRING = "mongodb://localhost:27017"
client = MongoClient(CONNECTION_STRING)
db=client[db_name]
collection = db['articles']


