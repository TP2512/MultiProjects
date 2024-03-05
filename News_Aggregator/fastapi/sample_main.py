from fastapi import FastAPI, HTTPException, status, Depends
from bson import ObjectId
from pydantic import BaseModel, EmailStr, field_validator
from pymongo.errors import DuplicateKeyError
from database.database_connection import get_database
from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import List


# MongoDB configuration
# MONGODB_URL = "mongodb://localhost:27017"
# DATABASE_NAME = "news_aggregator_db"
COLLECTION_NAME = "users"
# # Create MongoDB client
# client = AsyncIOMotorClient(MONGODB_URL)
# db = client[DATABASE_NAME]
# collection = db[COLLECTION_NAME]


# Pydantic model for user data
class User(BaseModel):
    username: str
    email: EmailStr

    @field_validator('username')
    def validate_username(cls, v):
        if not any(char.isalnum() for char in v):
            raise ValueError('Username must contain at least one alphanumeric character')
        if not any(char.isascii() and not char.isalnum() for char in v):
            raise ValueError('Username must contain at least one special character')
        if len(v) < 8:
            raise ValueError('Username must be at least 8 characters long')
        return v


# FastAPI app
app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Not Authorised"}


@app.get("/users", response_model=List[User])
async def get_user(db: AsyncIOMotorDatabase = Depends(get_database)):
    users = []
    async for user_data in db["users"].find():
        users.append(User(**user_data))
    return users


# Create user
@app.post("/users/")
async def create_user(user: User, db: AsyncIOMotorDatabase = Depends(get_database)):
    user_exists = await db["users"].find_one({"email": user.email})
    if user_exists:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email Already Exists")
    user_dict = user.dict()
    result = await db["users"].insert_one(user_dict)
    return {"id": str(result.inserted_id)}


# Delete user
@app.delete("/users/{user_id}")
async def delete_user(user_id: str, db: AsyncIOMotorDatabase = Depends(get_database)):
    result = await db["users"].delete_one({"_id": ObjectId(user_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted"}


# Update user
@app.put("/users/{user_id}")
async def update_user(user_id: str, user: User, db: AsyncIOMotorDatabase = Depends(get_database)):
    user_dict = user.dict()
    try:
        result = await db["users"].replace_one({"_id": ObjectId(user_id)}, user_dict)
        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="User not found")
        return {"message": "User updated"}
    except DuplicateKeyError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email Already Exists")
