from fastapi import FastAPI, HTTPException, status, Depends, Response
from bson import ObjectId
from pydantic import BaseModel, EmailStr, field_validator
from pymongo.errors import DuplicateKeyError
from database.database_connection import get_database
from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import List, Optional
from datetime import datetime
# from passlib.context import CryptContext
from utils import utils, oauth2
# handle InvalidId
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
from fastapi.security.oauth2 import OAuth2PasswordRequestForm


# Pydantic model for user data
class UserBase(BaseModel):
    username: str
    email: EmailStr
    password: str
    created_date: datetime = datetime.now()

    # noinspection PyMethodParameters
    @field_validator('username')
    def validate_username(cls, v):
        if not any(char.isalnum() for char in v):
            raise ValueError('Username must contain at least one alphanumeric character')
        if not any(char.isascii() and not char.isalnum() for char in v):
            raise ValueError('Username must contain at least one special character')
        if len(v) < 8:
            raise ValueError('Username must be at least 8 characters long')
        return v

    # noinspection PyMethodParameters
    @field_validator('password')
    def validate_password(cls, v, **kwargs):
        if not v:
            raise ValueError('Password cannot be Null')
        if not any(char.isascii() and not char.isalnum() for char in v):
            raise ValueError('password must contain at least one special character')
        if len(v) < 8:
            raise ValueError('password must be at least 8 characters long')
        if v == kwargs.get("username"):
            raise ValueError("Password cannot be the same as username")
        return v


class UserCreate(UserBase):
    pass


class UserResponse(BaseModel):
    id: str
    username: str
    email: EmailStr
    created_date: datetime


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None


# FastAPI app
app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Not Authorised"}


# Create user
@app.post("/user/", status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, db: AsyncIOMotorDatabase = Depends(get_database)):
    user_exists = await db["UserBase"].find_one({"email": user.email})
    if user_exists:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email Already Exists")
    user_exists = await db["UserBase"].find_one({"username": user.username})
    if user_exists:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username Already Exists")
    user_dict = user.dict()
    hashed_password = utils.get_hashed_password(user_dict["password"])
    user_dict["password"] = hashed_password
    result = await db["UserBase"].insert_one(user_dict)
    return UserResponse(id=str(result.inserted_id), username=user.username, email=user.email,
                        created_date=user_dict["created_date"])


# Get All Users
@app.get("/users", response_model=List[UserResponse], status_code=status.HTTP_200_OK)
async def get_user(db: AsyncIOMotorDatabase = Depends(get_database),
                   current_user: dict = Depends(oauth2.get_current_user)):
    if "admin" != current_user["username"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorised to perform requested action")
    users = []
    async for user_data in db["UserBase"].find():
        user_response = UserResponse(id=str(user_data["_id"]), username=user_data["username"], email=user_data["email"],
                                     created_date=user_data["created_date"])
        users.append(user_response)
    return users


# Get User Details
@app.get("/users/{user_id}", status_code=status.HTTP_200_OK)
async def get_user(user_id: str, db: AsyncIOMotorDatabase = Depends(get_database),
                   current_user: dict = Depends(oauth2.get_current_user)):
    if user_id != str(current_user["_id"]):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorised to perform requested action")
    user_data = await db["UserBase"].find_one({"_id": ObjectId(user_id)})
    if user_data:
        user_data["id"] = str(user_data["_id"])
        return UserResponse(id=str(user_data["id"]), username=user_data["username"], email=user_data["email"],
                            created_date=user_data["created_date"])
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User Not Found")


# Delete user
@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: str, db: AsyncIOMotorDatabase = Depends(get_database),
                      current_user: dict = Depends(oauth2.get_current_user)):
    if user_id != str(current_user["_id"]):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorised to perform requested action")
    result = await db["UserBase"].delete_one({"_id": ObjectId(user_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# Update user
@app.put("/users/{user_id}", status_code=status.HTTP_200_OK)
async def update_user(user_id: str, user: UserCreate, db: AsyncIOMotorDatabase = Depends(get_database),
                      current_user: dict = Depends(oauth2.get_current_user)):
    if user_id != str(current_user["_id"]):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorised to perform requested action")
    user_dict = user.dict()
    hashed_password = utils.get_hashed_password(user_dict["password"])
    user_dict["password"] = hashed_password
    try:
        result = await db["UserBase"].replace_one({"_id": ObjectId(user_id)}, user_dict)
        if result.modified_count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return {"message": "User updated"}
    except DuplicateKeyError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email Already Exists")


@app.post("/login")
async def login_user(user_credential: OAuth2PasswordRequestForm = Depends(),
                     db: AsyncIOMotorDatabase = Depends(get_database)):
    collection = db["UserBase"]
    user_by_email = await collection.find_one({"email": user_credential.username})
    user_by_username = await collection.find_one({"username": user_credential.username})
    if user_by_email is not None:
        user = user_by_email
    elif user_by_username is not None:
        user = user_by_username
    else:
        user = None
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")
    if not utils.verify(user_credential.password, user["password"]):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")
    access_token = oauth2.create_access_token(data={"user_id": str(user["_id"])})
    return {"access_token": access_token, "token_type": "Bearer"}
