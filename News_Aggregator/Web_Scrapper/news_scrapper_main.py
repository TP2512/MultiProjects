from bs4 import BeautifulSoup
import requests
from News_Aggregator import logger
from memory_profiler import profile


class WebScrapper:
    def __init__(self, url, parsing_strategy=None):
        self.url = url
        self._parsing_strategy = parsing_strategy or DefaultParsingStrategy()

    def fetch_page(self):
        try:
            response = requests.get(self.url)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            logger.error(f"Error while fetching page: {e}")
            return None

    # @profile
    def scrape(self):
        html = self.fetch_page()
        if html:
            data = self._parsing_strategy.parse_page(html)
            logger.info(f"Scraping completed successfully from {self.url}")
            return data
        else:
            logger.error(f"Failed to fetch page or parse html or url:{self.url}")
            return None


class ParsingStrategy:
    """This is abstract class"""
    def parse_page(self, html):
        """This is abstract method"""
        raise NotImplementedError


class DefaultParsingStrategy(ParsingStrategy):
    # @profile
    def parse_page(self, html):
        """This method is generator method which will give news at output one by one on call"""
        page_data = BeautifulSoup(html, 'html.parser')
        news_articles = page_data.find_all("div", class_="brief_box", attrs={"data-section_name": "/briefs"})
        for news in news_articles:
            data = {
                "title_element": news.find("h2"),
                "article_brief": news.find("p"),
                "category": news.find("p").a['href'].split('/')[1]
            }
            yield data


class WireParsingStrategy(ParsingStrategy):
    def parse_page(self, html):
        pass


if __name__ == "__main__":
    import time
    start_time = time.time()
    # @profile
    def main():
        news_url = "https://timesofindia.indiatimes.com/briefs"
        n_response = requests.get(news_url)
        soup = BeautifulSoup(n_response.text, 'html.parser')
        news_article = soup.find_all("div", class_="brief_box", attrs={"data-section_name": "/briefs"})

        for newss in news_article:
            title_element = newss.find("h2")
            article_brief = newss.find("p")
            category = article_brief.a['href'].split('/')[1]
            print("category: ", article_brief.a['href'].split('/')[1])
            print("title: ", title_element.text)
            print("full_content: ", article_brief.text)
            # print()
    main()
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Execution time: {execution_time} seconds")
