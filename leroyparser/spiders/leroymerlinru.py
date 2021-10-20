import scrapy
from scrapy.http import HtmlResponse
from leroyparser.items import LeroyparserItem
from scrapy.loader import ItemLoader


class LeroymerlinSpider(scrapy.Spider):
    name = 'leroumerlin'
    allowed_domains = ['leroymerlin.ru']

    def __init__(self, query):
        super().__init__()
        self.start_urls = [f'https://ufa.leroymerlin.ru/search/?q={query}']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath('//a[@data-qa-pagination-item="right"]/@href').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)


        links = response.xpath('//a[@data-qa="product-name"]')
        for link in links:
            yield response.follow(link, callback=self.parse_ads)


    def parse_ads(self, response:HtmlResponse):
        loader = ItemLoader(item=LeroyparserItem(), response=response)
        loader.add_value('link', response.url)
        loader.add_xpath('name', '//h1[@slot="title"]/text()')
        loader.add_xpath('price', '//span[@slot="price"]/text()')
        loader.add_xpath('photo', '//picture[@slot="pictures"]/source[contains(@data-origin,"w_2000")]/@srcset')
        loader.add_xpath('sp_title', '//dt[@class="def-list_term"]/text()')
        loader.add_xpath('sp_meaning', '//dd[@class="def-list_definition"]/text()')
        return loader.load_item()



