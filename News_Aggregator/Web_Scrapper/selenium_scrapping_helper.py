from bs4 import BeautifulSoup
import asyncio
import aiohttp


async def fetch_page(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()


async def scrape_article_details(article_url):
    html = await fetch_page(article_url)
    soup = BeautifulSoup(html, 'html.parser')
    try:
        news_article = soup.find_all("div", class_="story_details")
        paragraphs = news_article[0].find_all("p")
        article = ""
        for para in paragraphs:
            article += para.text
        data = {
            "headline": soup.find("h1", itemprop='headline').text,
            "description": soup.find("h2", itemprop='description').text,
            "date": soup.find("span", itemprop='dateModified').text,
            "article": article
        }
        print("news_data", data)
    except AttributeError:
        print("Failed to load article content")
    except IndexError:
        print(f"Failed to load article content:: url:{article_url}")


async def scrape_news_articles():
    main_url = "https://indianexpress.com/latest-news/"
    # html = requests.get("https://indianexpress.com/latest-news/").text
    html = await fetch_page(main_url)
    soup = BeautifulSoup(html, 'html.parser')
    all_divs = soup.find_all("div", class_="snaps")
    list_of_links = []
    for links in all_divs:
        article_url = links.a['href']
        list_of_links.append(article_url)
    tasks = [scrape_article_details(article_url) for article_url in list_of_links]
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    import time
    start_time = time.time()
    asyncio.run(scrape_news_articles())
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Execution time: {execution_time} seconds")
