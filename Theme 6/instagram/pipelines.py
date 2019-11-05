# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient

class InstagramPipeline(object):
    def __init__(self):
        mongo_url = 'mongodb://localhost:27017'
        client = MongoClient(mongo_url)
        instagram_bd = client['instagram_bd']
        self.instagram_collection = instagram_bd.instagram_following_and_posts
    def process_item(self, item, spider):
        self.instagram_collection.insert_one(item)
        return item
