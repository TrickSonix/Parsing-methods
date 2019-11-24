# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import scrapy
from scrapy.pipelines.images import ImagesPipeline
from pymongo import MongoClient

class AvitoParserPipeline(object):
    def __init__(self):
        mongo_url = 'mongodb://localhost:27017'
        client = MongoClient(mongo_url)
        avito_bd = client['avito_bd']
        self.avito_collection = avito_bd.avito_cars
    def process_item(self, item, spider):
        self.avito_collection.insert_one(item)
        return item

class AvitoPhotosPipeline(ImagesPipeline):

    def get_media_request(self, item, info):
        if item['photos']:
            for img in item['photos']:
                try:
                    scrapy.Request(img)
                except Exception as e:
                    pass
    def item_completed(self, result, item, info):
        if result:
            item['photos'] = [itm[1] for itm in result if itm[0]]
        return item