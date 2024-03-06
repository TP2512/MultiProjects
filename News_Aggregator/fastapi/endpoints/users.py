from fastapi import HTTPException, status, Depends, Response, APIRouter
from bson import ObjectId
from pymongo.errors import DuplicateKeyError
from ..database.database_connection import get_database
from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import List
from ..models import schema as sc

router = APIRouter()


# Create user
@router.post("/user/", status_code=status.HTTP_201_CREATED)
async def create_user(user: sc.UserCreate, db: AsyncIOMotorDatabase = Depends(get_database)):
    # print("In Post")
    user_exists = await db["UserBase"].find_one({"email": user.email})
    if user_exists:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email Already Exists")
    user_dict = user.dict()
    result = await db["UserBase"].insert_one(user_dict)
    # return {"id": str(result.inserted_id)}
    return sc.UserResponse(id=str(result.inserted_id), username=user.username, email=user.email,
                        created_date=user_dict["created_date"])


# Get All Users
@router.get("/users", response_model=List[sc.UserResponse], status_code=status.HTTP_200_OK)
async def get_user(db: AsyncIOMotorDatabase = Depends(get_database)):
    users = []
    async for user_data in db["UserBase"].find():
        user_response = sc.UserResponse(id=str(user_data["_id"]), username=user_data["username"], email=user_data["email"],
                                     created_date=user_data["created_date"])
        users.append(user_response)
    return users


# Get User Details
@router.get("/users/{user_id}", status_code=status.HTTP_200_OK)
async def get_user(user_id: str, db: AsyncIOMotorDatabase = Depends(get_database)):
    user_data = await db["UserBase"].find_one({"_id": ObjectId(user_id)})
    if user_data:
        user_data["id"] = str(user_data["_id"])
        return sc.UserResponse(id=str(user_data["id"]), username=user_data["username"], email=user_data["email"],
                            created_date=user_data["created_date"])
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User Not Found")


# Delete user
@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: str, db: AsyncIOMotorDatabase = Depends(get_database)):
    result = await db["UserBase"].delete_one({"_id": ObjectId(user_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# Update user
@router.put("/users/{user_id}", status_code=status.HTTP_200_OK)
async def update_user(user_id: str, user: sc.UserCreate, db: AsyncIOMotorDatabase = Depends(get_database)):
    user_dict = user.dict()
    try:
        result = await db["UserBase"].replace_one({"_id": ObjectId(user_id)}, user_dict)
        if result.modified_count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return {"message": "User updated"}
    except DuplicateKeyError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email Already Exists")

