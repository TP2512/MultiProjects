from pydantic import BaseModel, field_validator, EmailStr
from typing import Optional
from datetime import datetime


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
