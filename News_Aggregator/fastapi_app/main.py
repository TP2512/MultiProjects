from endpoints import users, auth
from fastapi import FastAPI


app = FastAPI()

app.include_router(users.router)
app.include_router(auth.router)

@app.get("/")
async def root():
    return {"message": "Not Authorised"}
