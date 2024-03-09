import requests as rq


class SentimentAnalysis:
    def __init__(self, news):
        self.news = news
        self._url = "http://127.0.0.1:8001/get_sentiment"

    def get_sentiment_from_app(self):
        try:
            response = rq.post(self._url, json={"news_article": self.news})
            return response.json()
        except Exception as e:
            return e
