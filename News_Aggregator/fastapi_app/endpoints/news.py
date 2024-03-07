from fastapi import HTTPException, status, Depends, APIRouter
from database.database_connection import get_database
from motor.motor_asyncio import AsyncIOMotorDatabase
from utils import utils, oauth2
from models import schema as sc


router = APIRouter()


@router.post("/user/", status_code=status.HTTP_201_CREATED)
async def create_user(user: sc.UserCreate, db: AsyncIOMotorDatabase = Depends(get_database)):
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
    return sc.UserResponse(id=str(result.inserted_id), username=user.username, email=user.email,
                        created_date=user_dict["created_date"])
