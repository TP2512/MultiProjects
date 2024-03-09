from fastapi import APIRouter, Depends, status, HTTPException
from database import database_connection as dc
from motor.motor_asyncio import AsyncIOMotorDatabase
from utils import utils, oauth2
from fastapi.security.oauth2 import OAuth2PasswordRequestForm


router = APIRouter(tags=['Authentication'])


@router.post("/login")
async def login_user(user_credential: OAuth2PasswordRequestForm = Depends(),
                     db: AsyncIOMotorDatabase = Depends(dc.get_database)):
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