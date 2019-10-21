# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient

class HhParserPipeline(object):
    def __init__(self):
        mongo_url = 'mongodb://localhost:27017'
        client = MongoClient(mongo_url)
        hh_db = client['hh_db']
        self.hh_collection = hh_db.hh_vacancy
    def process_item(self, item, spider):
        self.hh_collection.insert_one(item)
        return item
