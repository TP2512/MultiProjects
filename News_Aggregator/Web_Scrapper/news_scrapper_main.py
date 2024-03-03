from News_Aggregator import logger
# from memory_profiler import profile
import requests
from bs4 import BeautifulSoup
import aiohttp


class WebScrapper:
    def __init__(self, url, parsing_strategy=None):
        self.url = url
        self._parsing_strategy = parsing_strategy or DefaultParsingStrategy()

    async def fetch_page(self):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.url) as response:
                    return await response.text()
        except requests.RequestException as e:
            logger.error(f"Error while fetching page: {e}")
            return None
        except aiohttp.ClientConnectorError as e:
            logger.error("Internet Connection is broken")

    # @profile
    async def scrape(self):
        html = await self.fetch_page()
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
                "source": "TOI",
                "title": news.find("h2").text,
                "content": news.find("p").text,
                # "category": news.find("p").a['href'].split('/')[1]
            }
            yield data


class IEParsingStrategy(ParsingStrategy):
    def parse_page(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        try:
            news_article = soup.find_all("div", class_="story_details")
            paragraphs = news_article[0].find_all("p")
            article = ""
            for para in paragraphs:
                article += para.text
            data = {
                "source": "IE",
                "title": soup.find("h1", itemprop='headline').text,
                # "description": soup.find("h2", itemprop='description').text,
                # "date": soup.find("span", itemprop='dateModified').text,
                "content": article
            }
            yield data
        except AttributeError:
            logger.error("Failed to load article content")
        except IndexError:
            logger.error(f"Failed to load article content")


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
            # category = article_brief.a['href'].split('/')[1]
            print("category: ", article_brief.a['href'].split('/')[1])
            print("title: ", title_element.text)
            print("full_content: ", article_brief.text)
    main()
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Execution time: {execution_time} seconds")
