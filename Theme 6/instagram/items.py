# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class InstagramItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    user = scrapy.Field()
    following = scrapy.Field()
    filtered_posts = scrapy.Field()