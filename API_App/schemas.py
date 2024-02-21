from pydantic import BaseModel
import datetime


class Post(BaseModel):
    Title: str
    Author: str = "Anonymous"
    Description: str | None = None
    Published_date: datetime.now()
    Likes: int | None = None

class User(BaseModel):
    Username: email
    Password: str
    Created_at: datetime.now()


