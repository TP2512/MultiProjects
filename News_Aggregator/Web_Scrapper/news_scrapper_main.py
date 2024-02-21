from bs4 import BeautifulSoup
import requests
from .. import logger


class WebScrapper:
    def __init__(self, url, parsing_strategy=None):
        self.url = url
        self.parsing_strategy = parsing_strategy | DefaultParsingStrategy()

    def fetch_page(self):
        try:
            response = requests.get(self.url)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            logger.error(f"Error while fetching page: {e}")
            return None

    def scrape(self):
        html = self.fetch_page()
        if html:
            data = self.parsing_strategy.parse_page(html)
            logger.info("Scraping completed successfully")
            return data
        else:
            logger.error("Failed to fetch page or parse html")
            return None


class ParsingStrategy:
    def parse_page(self, html):
        raise NotImplementedError


class DefaultParsingStrategy(ParsingStrategy):
    def parse_page(self, html):
        page_data = BeautifulSoup(html.text, 'html.parser')
        news_article = page_data.find_all("div", class_="brief_box", attrs={"data-section_name": "/briefs"})
        return news_article


class WireParsingStrategy(ParsingStrategy):
    def parse_page(self, html):
        pass


if __name__ == "__main__":
    news_url = "https://timesofindia.indiatimes.com/briefs"
    n_response = requests.get(news_url)
    soup = BeautifulSoup(n_response.text, 'html.parser')
    news_articles = soup.find_all("div", class_="brief_box", attrs={"data-section_name": "/briefs"})

    for news in news_articles:
        title_element = news.find("h2")
        article_brief = news.find("p")
        category = article_brief.a['href'].split('/')[1]
        print("category: ", article_brief.a['href'].split('/')[1])
        print("title: ", title_element.text)
        print("full_content: ", article_brief.text)
        print()
