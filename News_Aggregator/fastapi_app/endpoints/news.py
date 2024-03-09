from fastapi import HTTPException, status, Depends, APIRouter
from utils import oauth2
from models import schema as sc
from services import get_sentiment as gs

router = APIRouter()


@router.post("/get_sentiment_from_news", response_model=sc.NewsResponse, status_code=status.HTTP_200_OK)
async def get_sentiment_from_news(news: sc.NewsInput, current_user: dict = Depends(oauth2.get_current_user)):
    try:
        senti_getter = gs.SentimentAnalysis(news.news_article)
        senti_of_news = senti_getter.get_sentiment_from_app()
        return sc.NewsResponse(sentiment=senti_of_news)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
