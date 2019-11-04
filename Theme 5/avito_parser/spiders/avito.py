# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader import ItemLoader
from avito_parser.items import AvitoParserItem
import json

class AvitoSpider(scrapy.Spider):
    name = 'avito'
    allowed_domains = ['avito.ru']
    start_urls = ['https://www.avito.ru/moskva/avtomobili']

    def parse(self, response):
        next_link = response.xpath('//div[contains(@class, "pagination-nav")]/a[contains(@class, "js-pagination-next")]/@href').extract_first()
        yield response.follow(next_link, callback=self.parse)

        auto_links = response.xpath('//div[contains(@class, "item")]//a[@class="item-description-title-link"]/@href').extract()
        for auto in auto_links:
            yield response.follow(auto, callback=self.parse_auto_page)

    def parse_auto_page(self, response):
        item = ItemLoader(AvitoParserItem(), response)
        item.add_xpath('title', '//h1[@class="title-info-title"]/span[@class="title-info-title-text"]/text()')
        item.add_xpath('price', '//div[@class="item-price-value-wrapper"]//span[@class="js-item-price"]/@content')
        item.add_xpath('params', '//div[@class="item-params"]/ul[@class="item-params-list"]/li')
        item.add_xpath('photos', '//div[contains(@class, "gallery-img-wrapper")]/div[contains(@class, "gallery-img-frame")]/@data-url')
        autoteka_link_id = response.xpath('//div[@class="js-autoteka-teaser"]/@data-item-id').extract_first()
        autoteka_link = 'https://www.avito.ru/web/1/swaha/v1/autoteka/teaser/'
        yield response.follow(autoteka_link+autoteka_link_id, callback=self.get_VIN_official, meta={'item': item})

    def get_VIN_official(self, response):
        item = response.meta['item']
        result = json.loads(response.text)
        if result:
            item.add_value('VIN_official', result['result']['insights'])
        else:
            item.add_value('VIN_official', result['error'])
        yield item.load_item()
