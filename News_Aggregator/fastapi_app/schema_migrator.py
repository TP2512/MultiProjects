import json
from pymongo import MongoClient
from sample_main import UserBase


def create_model_metadata():
    # Generate schema metadata for the Pydantic model
    model_schema = UserBase.schema()

    # Serialize the metadata to a JSON file
    with open("model_metadata.json", "w") as f:
        json.dump(model_schema, f)

    print("Model metadata created successfully.")


def check_model_metadata_changes():
    # Load the previously stored metadata
    with open("model_metadata.json", "r") as f:
        stored_metadata = json.load(f)

    # Generate the current metadata for the Pydantic model
    current_metadata = UserBase.schema()

    # Compare the stored metadata with the current metadata
    if stored_metadata != current_metadata:
        print("Model metadata has changed. Updating MongoDB collection...")
        # Run your script to update the MongoDB collection with the new validation rules
        update_mongodb_collection()
    else:
        print("no changes in metadata")


# MongoDB connection settings
MONGODB_URI = "mongodb://localhost:27017/"
DB_NAME = "news_aggregator_db"
COLLECTION_NAME = "UserBase"

# Validation rules for the collection
VALIDATION_RULES = {
    "validator": {
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["username", "password", "email"],
            "properties": {
                "username": {
                    "bsonType": "string",
                    "minLength": 8,
                    "pattern": "^(?=.*[a-zA-Z])(?=.*[!@#$%^&*()_+\-=\[\]{};:\'\"<>,./?])(?=.*[0-9])[a-zA-Z0-9!@#$%^&*()_+\-=\[\]{};:\'\"<>,./?]{8,}$",
                    "description": "must be a string and contain at least one alphanumeric character, one special character, and be at least 8 characters long"
                },
                "email": {
                    "bsonType": "string",
                    "description": "must be a valid email address"
                },
                "password": {
                    "bsonType": "string",
                    "minLength": 8,
                    "pattern": "^(?=.*[a-zA-Z])(?=.*[!@#$%^&*()_+\-=\[\]{};:\'\"<>,./?])(?=.*[0-9])[a-zA-Z0-9!@#$%^&*()_+\-=\[\]{};:\'\"<>,./?]{8,}$",
                    "description": "must be a string and contain at least one alphanumeric character, one special character, and be at least 8 characters long"
                }
            }
        }
    },
    "validationLevel": "strict",  # Rejects documents that do not meet the validation criteria
    "validationAction": "error"    # Returns an error if a document violates the validation rules
}


def update_mongodb_collection():
    # Connect to MongoDB
    client = MongoClient(MONGODB_URI)
    db = client[DB_NAME]

    # Create collection based on Pydantic model class name
    collection_name = UserBase.__name__

    # Update collection options to apply validation rules
    # db.command("collMod", COLLECTION_NAME, **VALIDATION_RULES)

    if collection_name in db.list_collection_names():
        # Delete collection if it already exists
        db.drop_collection(collection_name)
        print(f"Collection '{collection_name}' deleted.")

    # Create collection
    db.create_collection(collection_name, **VALIDATION_RULES)
    print(f"Collection '{collection_name}' created.")
    print(f"Validation rules added to collection '{COLLECTION_NAME}'.")
    db[collection_name].create_index("email", unique=True)
    print("Unique index created on the 'email' field.")


if __name__ == "__main__":
    # Check if the model metadata file exists
    try:
        with open("model_metadata.json", "r") as f:
            metadata_exists = True
    except FileNotFoundError:
        metadata_exists = False

    if not metadata_exists:
        create_model_metadata()
        update_mongodb_collection()
    else:
        check_model_metadata_changes()
