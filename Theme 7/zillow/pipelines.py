# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient

class ZillowPipeline(object):
    def __init__(self):
        mongo_url = 'mongodb://localhost:27017'
        client = MongoClient(mongo_url)
        zillow_bd = client['zillow_bd']
        self.zillow_collection = zillow_bd.zillow_houses
    def process_item(self, item, spider):
        self.zillow_collection.insert_one(item)
        return item
