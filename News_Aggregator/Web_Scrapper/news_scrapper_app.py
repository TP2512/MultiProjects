import requests
from News_Aggregator import logger
from bs4 import BeautifulSoup
from News_Aggregator.Web_Scrapper import news_scrapper_main as nws
import time
import asyncio
from Web_Scrapper.Database import mongodb_connection as mc
from datetime import datetime

db_handler = mc.MongoDBConnection("news_aggregator_db", "news_articles")


def push_to_mongodb(data):
    data.update({"created_date": datetime.now(), "user": "webscraper"})
    # data.update({"sentiment": get_sentiment(data["content"])})
    result = db_handler.collection.insert_one(data)
    print(f"Inserted news article with ID: {result.inserted_id}")


async def scrape_and_push(url, parser=None):
    try:
        scrapper = nws.WebScrapper(url, parser)
        news_articles = await scrapper.scrape()
        print(url.split('.')[0].split('/')[-1], ":")
        for article in news_articles:
            # push_to_mongodb(article)
            print(article)
    except TypeError:
        print(f"Internet connection is broken or url dont have any relative content {url}")
        logger.error(f"Internet connection is broken or url dont have any relative content {url}")


async def main():
    await asyncio.gather(*[scrape_and_push(url, parser) for url, parser in urls])


urls = [
        ("https://timesofindia.indiatimes.com/briefs", nws.DefaultParsingStrategy())
    ]
start_time = time.time()

main_page = requests.get("https://indianexpress.com/latest-news/")
soup = BeautifulSoup(main_page.text, 'html.parser')
all_divs = soup.find_all("div", class_="snaps")
for links in all_divs:
    art_url = links.a['href']
    urls.append((art_url, nws.IEParsingStrategy()))
print("total_links", len(urls))
asyncio.run(main())
end_time = time.time()
execution_time = end_time - start_time
print(f"Execution time: {execution_time} seconds")
