from pprint import pprint
from lxml import html
import requests
from pymongo import MongoClient

client = MongoClient('127.0.0.1', 27017)
db = client['yandex_news']
collection = db.all_news

header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36'}

response = requests.get("https://yandex.ru/sport?utm_source=yxnews&utm_medium=desktop")
dom = html.fromstring(response.text)

items = dom.xpath("//div[contains(@class,'sport-app__top')]")
all_news =[]
for item in items:
    news = {}
    name = dom.xpath(".//h2[@class='mg-card__title']/text()")
    source = dom.xpath(".//a[@aria-label]//text()")
    link = dom.xpath(".//h2[@class='mg-card__title']/../@href")
    date = dom.xpath(".//span[@class='mg-card-source__time']/text()")

    news['name'] = name
    news['link'] = link
    news['source'] = source
    news['date'] = date
    all_news.append(news)

    pprint(news)

collection.insert_many(all_news)
