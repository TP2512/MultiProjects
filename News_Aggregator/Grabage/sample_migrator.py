from pymongo import MongoClient
from pymongo.errors import CollectionInvalid
from sample_main import User


# MongoDB connection settings
MONGODB_URI = "mongodb://localhost:27017/"
DB_NAME = "news_aggregator_db"


def create_database_and_collection():
    # Connect to MongoDB
    client = MongoClient(MONGODB_URI)
    db = client[DB_NAME]

    # Create collection based on Pydantic model class name
    collection_name = User.__name__

    if collection_name in db.list_collection_names():
        # Delete collection if it already exists
        db.drop_collection(collection_name)
        print(f"Collection '{collection_name}' deleted.")

    # Create collection
    db.create_collection(collection_name)
    print(f"Collection '{collection_name}' created.")

if __name__ == "__main__":
    create_database_and_collection()
