import requests
from bs4 import BeautifulSoup
from News_Aggregator import logger
from News_Aggregator.Web_Scrapper import news_scrapper_main as nws
import time
import asyncio
from pymongo import MongoClient
import concurrent.futures

def push_to_mongodb(data):
    client = MongoClient("mongodb://localhost:27017/")
    db = client["news_db"]
    collection = db["news_collection"]
    result = collection.insert_one(data)
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
        print(f"Internet connection is broken or url don't have any relevant content: {url}")
        logger.error(f"Internet connection is broken or url don't have any relevant content: {url}")

async def main():
    tasks = []
    with concurrent.futures.ProcessPoolExecutor() as pool:
        loop = asyncio.get_event_loop()
        for url, parser in urls:
            tasks.append(loop.run_in_executor(pool, scrape_and_push, url, parser))
        await asyncio.gather(*tasks)

start_time = time.time()
urls = [("https://timesofindia.indiatimes.com/briefs", nws.DefaultParsingStrategy())]
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
