from bs4 import BeautifulSoup
import requests
from .. import logger
from . import news_scrapper_main

urls=[
    ("https://timesofindia.indiatimes.com/briefs",)
]






url=

response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
news_articals=soup.find_all("div",class_="brief_box",attrs={"data-section_name":"/briefs"})

for news in news_articals:
    title_element = news.find("h2")
    article_brief = news.find("p")
    category = article_brief.a['href'].split('/')[1]
    print("category: ",article_brief.a['href'].split('/')[1])
    print("title: ",title_element.text)
    print("full_content: ",article_brief.text)
    print()

