from News_Aggregator import logger
from News_Aggregator.Web_Scrapper import news_scrapper_main as nws
import time

start_time = time.time()

urls = [
    ("https://timesofindia.indiatimes.com/briefs", nws.DefaultParsingStrategy()),
    ("https://thewire.com", nws.WireParsingStrategy())
]

for url, parser in urls:
    scraper = nws.WebScrapper(url, parser)
    news_article = scraper.scrape()
    if news_article:
        for news in news_article:
            print(news.get("article_brief").text)
            print()
    else:
        logger.warning(f"no data scrapped from {url}")

end_time = time.time()
execution_time = end_time - start_time
print(f"Execution time: {execution_time} seconds")
