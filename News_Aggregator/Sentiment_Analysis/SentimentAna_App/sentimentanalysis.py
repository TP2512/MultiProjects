from pydantic import BaseModel
from fastapi import FastAPI
from typing import Text
from service import setment_responder as sr

app = FastAPI()


class NewsInput(BaseModel):
    news_article: Text


@app.post("/get_sentiment")
async def get_sentiment(news:  NewsInput):
    sg = sr.NewsAnalysis(news.news_article)
    return sg.sentiment_getter()
