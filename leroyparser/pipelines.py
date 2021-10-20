# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import hashlib
import scrapy
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline
from leroyparser.items import LeroyparserItem
from scrapy.utils.python import to_bytes
from pymongo import MongoClient
from PIL import Image

class LeroyparserPipeline:
    def __init__(self):
        client = MongoClient('127.0.0.1', 27017)
        self.mongo_base = client.leroymerlin

    def process_item(self, item, spider):
        collection = self.mongo_base[spider.name]
        item['sp'] = self.create_specific(item['sp_meaning'], item['sp_title'])
        del item['sp_meaning']
        del item['sp_title']
        collection.inseart_many(item)
        return ()

    def create_specific(self, meaning, title):
        data = {}
        for index, item in enumerate(title):
            data[item] = meaning[index]
        return data


class LeroyPhotosPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item['photo']:
            for img in item['photo']:
                try:
                    yield scrapy.Request(img)
                except Exception as e:
                    print(e)

    def item_completed(self, results, item, info):
        item['photo'] = [itm[1] for itm in results if itm[0]]
        return item

    def file_path(self, request, response=None, info=None, *, item=LeroyparserItem ):
        image_quid = request.url.split('/')[-1]
        img_path = item['link'].split('-')[-1]
        return f'{img_path}{image_quid}'