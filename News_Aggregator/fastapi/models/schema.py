from pydantic import BaseModel, field_validator, EmailStr, constr
from typing import Optional
from datetime import datetime
from News_Aggregator.fastapi.database import database_connection as dc


class NewsFeed(BaseModel):
    id: Optional[int]
    title: Optional[str]
    news: Optional[str]
    created_date: Optional[str]

    @field_validator('news')
    def check_content_length(cls, v):
        if v and len(v.split()) > 200:
            raise ValueError("Content should not exceed 200 words")
        return v

    @field_validator('*')
    def check_at_least_one_input_given(cls, values):
        if not any(values.values()):
            raise ValueError("'At least one input field (title, news, created_date) must be provided")
        return values


class SentimentAnalysis(BaseModel):
    polarity: float
    subjectivity: float


class NewsResponse(BaseModel):
    id: int
    title: Optional[str]
    sentiment: SentimentAnalysis


class UserCreate(BaseModel):
    username: constr(regex=r'^[a-zA-Z0-9]*[!@#$%^&*()_+=\-[\]{};:\'"<>?,./\\|`~]*[a-zA-Z0-9]*$')
    email: EmailStr
    password: str
    created_date: datetime.now()

    @field_validator('username')
    def username_check(cls, v):
        if len(v) < 8:
            raise ValueError("username must be atleast 8 chars")
        return v

    @field_validator('email')
    def check_email_exists(cls, v):
        db = dc.get_database()
        existing_user = db["users"].find_one({"email": v})
        if existing_user:
            raise ValueError("Email Already exists")


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime


class UserLogin(BaseModel):
    email: EmailStr
    password: str
