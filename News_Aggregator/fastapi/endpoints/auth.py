from fastapi import APIRouter, Depends, status, HTTPException, Response
from News_Aggregator.fastapi.database import database_connection as dc
from motor.motor_asyncio import AsyncIOMotorDatabase
from News_Aggregator.fastapi.models import schema as sc

router = APIRouter(tags=['Authentication'])


@router.post("/login")
async def login_user(user_credential: sc.UserLogin, db: AsyncIOMotorDatabase = Depends(dc.get_database)):
    collection = db["users"]
    user = await collection.find_one({"email": user_credential.email})
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid credentials")
    return {"data": data}
