# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import TakeFirst, MapCompose

def params_processor(item):
    key = item.split('>')[-3].split(':')[0]
    value = item.split('>')[-2].split(' ')[0]
    return {key: value}

def dict_params(item):
    result = {}
    for itm in item:
        result.update(itm)
    return result

def photos_processor(item):
    if item[:2] == '//':
        return f'http:{item}'
    return item

class AvitoParserItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    _id = scrapy.Field()
    title = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(output_processor=TakeFirst())
    params = scrapy.Field(input_processor=MapCompose(params_processor), output_processor=dict_params)
    VIN_official = scrapy.Field()
    photos = scrapy.Field(input_processor=MapCompose(photos_processor))

