# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose

def photos_processor(item):
    return item.split(' ')[-2]

def title_processor(item):
    return item[0] + item[2]

def params_processor(item):
    result = {}
    for i in len(item)/2:
        result[item[i][:-1]] = item[i+1]
    return result

class ZillowItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    _id = scrapy.Field()
    photos = scrapy.Field(input_processor=MapCompose(photos_processor))
    title = scrapy.Field(input_processor=title_processor)
    params = scrapy.Field(input_processor=params_processor)
    description = scrapy.Field()

