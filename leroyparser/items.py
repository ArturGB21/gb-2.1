# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import MapCompose, TakeFirst, Compose
import re


def int_price(value):
    try:
        value = int(value)
    except Exception as e:
        return value
    return value
def clear_meaning(value):
    value = value.replase('\n',' ').replase(' ','')
    return value


class LeroyparserItem(scrapy.Item):
    name = scrapy.Field(output_processor=TakeFirst())
    link = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(input_processor=MapCompose(int_price), output_processor=TakeFirst())
    photo = scrapy.Field()
    sp_title = scrapy.Field()
    sp_meaning = scrapy.Field(input_processor=MapCompose(clear_meaning))
    sp = scrapy.Field()
    _id = scrapy.Field()
