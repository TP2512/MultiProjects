from pydantic import BaseModel
from fastapi import FastAPI
from typing import Text
from service import setment_responder as sr
from loggers import configure_logger


logger = configure_logger()
app = FastAPI()


class NewsInput(BaseModel):
    news_article: Text


@app.post("/get_sentiment")
async def get_sentiment(news:  NewsInput):
    sg = sr.NewsAnalysis(news.news_article)
    logger.info("got request for sentiment from news")
    return sg.sentiment_getter()
