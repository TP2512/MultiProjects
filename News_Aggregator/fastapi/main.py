from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()
# uvicorn main:app --reload


class User(BaseModel):
    id: int
    name: str
    email: str


users_db = {
    1: User(id=1, name="Alice", email="alice@example.com"),
    2: User(id=2, name="Bob", email="bob@example.com"),
}


@app.get("/")
async def root():
    return {"message": "please login for more information"}


@app.get("/users")
async def get_all_user():
    users_list = list(users_db.values())
    return {"users": users_list}


@app.get("/user/{user_id}")
async def get_user_det(user_id: int):
    user_det = users_db.get(user_id)
    return {"user details": user_det}


@app.post("/user")
async def add_user(user: User):
    if user.id in users_db:
        raise HTTPException(status_code=400, detail="user already exists")
    users_db[user.id] = user
    return {"user": user}


# PUT endpoint to update a user
@app.put("/user/{user_id}")
async def update_user(user_id: int, user: User):
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    users_db[user_id] = user
    return user


# PATCH endpoint to partially update a user
@app.patch("/user/{user_id}")
async def partial_update_user(user_id: int, user_patch: User):
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    user = users_db[user_id]
    update_data = user_patch.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(user, key, value)
    return user


@app.delete("/user/{user_id}")
async def user_delete(user_id: int):
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="user not found")
    del users_db[user_id]
    return {"message": "user has been deleted successfully"}
